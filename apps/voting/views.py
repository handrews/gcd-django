import hashlib
import os.path
from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django.core import urlresolvers
from django.core.mail import send_mail
from django.core.files import File
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from apps.gcd.views import render_error
from apps.voting.models import *

EMAIL_RESULT = """
All ballots have been received for the following topic from the %s agenda:

  %s

The results are:

%s

Please go to %s for more details.
"""

EMAIL_RECEIPT = """
This is your receipt for your vote in the secret ballot election for %s.
You voted for:
%s

If anything has gone wrong with your vote, or if the election allows you to
change your vote and you wish to change it, you will need to provide the
following two pieces of information to the voting administrator (%s)
in order to match account to your votes.  Note that changing your vote
may require you to disclose your vote choices to the voting administrator.

secret key:
'%s'
vote id:
'%s'
"""

def _classify_topics(topics, user):
    # Permissions are returned as appname.codename by get_all_permissions().
    if user.is_anonymous():
        my_topics = ()
        forbidden_topics = topics
    elif user.is_superuser:
        # Superusers have all permissions, which can be very expensive in
        # the else clause.  Non-superusers tend to have just a few permissions.
        my_topics = topics
        forbidden_topics = ()
    else:
        q_list = []
        # You can't actually get a query_set of the user's permissions, just this
        # list of strings that stuff the app label and code name together.  So
        # we have to build queries that match each of the actual permissions, and
        # then OR those all together.
        for p in user.get_all_permissions():
            app_label, code_name = p.split('.', 1)
            q_list.append(Q(agenda__permission__codename=code_name,
                            agenda__permission__content_type__app_label=app_label))

        can_vote = reduce(lambda x, y: x | y, q_list)
        my_topics = topics.filter(can_vote)
        forbidden_topics = topics.exclude(can_vote)

    voted_topics = []
    pending_topics = []
    for topic in my_topics:
        if topic.has_vote_from(user):
            voted_topics.append(topic)
        else:
            pending_topics.append(topic)
    return (pending_topics, voted_topics, forbidden_topics)

def dashboard(request):
    topics = Topic.objects.filter(deadline__gte=datetime.now(), open=True)

    # We ignore the forbidden topics on the dashboard and only show relevant topics.
    pending_topics, voted_topics, forbidden_topics = \
      _classify_topics(topics, request.user)
    return render_to_response('voting/dashboard.html',
                              {
                                'voted_topics': voted_topics,
                                'pending_topics': pending_topics,
                                'agendas': Agenda.objects.all(),
                              },
                              context_instance=RequestContext(request))

def _calculate_results(unresolved):
    """
    Given a QuerySet of unresolved topics (with expired deadlines),
    resolve them into results, possibly indicating a tie of some sort.

    TODO: Handle ranked choice voting.
    TODO: Handle the case of abstaning being a "winning" option.
    """

    for topic in unresolved:
        explanation = topic.calculate_results()
        if explanation:
            explanation = '\n\n' + explanation
        _send_result_email(topic, explanation)

def _send_result_email(topic, extra=''):
    for list_config in topic.agenda.agenda_mailing_lists.all():
        if list_config.on_vote_close:
            result = None
            if topic.invalid:
                result = ('This vote failed to produce a valid result, '
                          'possibly because of a tie.  '
                          'The vote administrators will follow up as needed.')
            elif topic.vote_type.name in (TYPE_PASS_FAIL, TYPE_CHARTER):
                result_name = topic.options.get(result=True).name
                if result_name == 'For':
                    result = 'The motion PASSED'
                elif result_name == 'Against':
                    result = 'The motion FAILED'

            if result is None:
                # Either it's not a pass/fail or charter, or the options
                # were renamed so we can't convert to PASS/FAIL.
                result = 'The following option(s) won:\n'
                for winner in topic.options.filter(result=True):
                    result += '  * %s\n' % winner.name

            result += extra
            email_body = EMAIL_RESULT % (topic.agenda, topic.text, result,
              settings.SITE_URL.rstrip('/') + topic.agenda.get_absolute_url())

            list_config.send_mail(subject="GCD Vote Result: %s" % topic,
                                  message=email_body)

@login_required
def topic(request, id):
    topic = get_object_or_404(Topic, id=id)

    if not request.user.has_perm('gcd.can_vote'):
        return render_error(request,
                            'You do not have permission to vote on this topic.')
    # Note that if this was a secret ballot, this will be an empty
    # queryset.  That is OK, the UI won't look at it in that case.
    # But this is why "voted" is not just a check for at least one vote here.
    votes = topic.options.filter(votes__voter=request.user)

    return render_to_response('voting/topic.html',
                              {
                                'topic': topic,
                                'voted': topic.has_vote_from(request.user),
                                'votes': votes,
                                'closed': topic.deadline < datetime.now(),
                                'settings': settings,
                              },
                              context_instance=RequestContext(request))

@permission_required('gcd.can_vote')
def vote(request):
    if request.method != 'POST':
        return render_error(request,
                            'Please access this page through the correct form.')

    first = True
    topic = None
    voter = None
    option_params = request.POST.getlist('option')
    options = Option.objects.filter(id__in=option_params)

    # Get all of these now because we may need to iterate twice.
    options = options.select_related('topic__agenda', 'topic__vote_type').all()
    if not options:
        return render_error(request,
                            'You must choose at least one option to vote.')
    for option in options:
        if first is True:
            first = False
            topic = option.topic

            if not request.user.has_perm('%s.%s' %
                (topic.agenda.permission.content_type.app_label,
                 topic.agenda.permission.codename)):
                return render_error(request,
                  'We are sorry, but you do not have permission to vote '
                  'on this ballot.  You must have the "%s" permission.' %
                   topic.agenda.permission.name)

            if topic.token is not None and \
               request.POST['token'].strip() != topic.token:
                return render_error(request,
                  'You must supply an authorization token in order '
                  'to vote on this topic.')

            if topic.vote_type.max_votes is not None and \
               len(option_params) > topic.vote_type.max_votes:
                plural = 's' if len(option_params) > 1 else ''
                return render_error(request,
                  'You may not vote for more than %d option%s' %
                  (topic.vote_type.max_votes, plural))

            if topic.agenda.secret_ballot:
                receipts = Receipt.objects.filter(topic=topic, voter=request.user)
                already_voted = receipts.count() > 0
            else:
                voter = request.user
                already_voted = Vote.objects.filter(option__topic=topic,
                                                    voter=request.user).count() > 0

            if already_voted:
                return render_error(request,
                  'You have already voted on this ballot.  If you wish to change '
                  'your vote, please contact the voting administrator at ' +
                  settings.EMAIL_VOTING_ADMIN)

        # Ranked voting not yet supported (no UI) so just set rank to None.
        vote = Vote(option=option, voter=voter, rank=None)
        vote.save()

    if topic.agenda.secret_ballot:
        # We email the salt and the vote string to the voter, and store
        # the receipt key in the database.  This way they can prove that
        # they voted a particular way by sending us back those two values,
        # and repair or change a vote.
        vote_ids = ', '.join(option_params)
        salt = hashlib.sha1(str(random())).hexdigest()[:5]
        key = hashlib.sha1(salt + vote_ids).hexdigest()

        receipt = Receipt(voter=request.user,
                          topic=option.topic,
                          vote_key=key)
        receipt.save()

        # Log the data as a backup in case of mail sending/receiving problems.
        # Technically, this makes it not a secret ballot, but it takes some
        # work to interpret the log, and there's always been a human counting
        # the ballots before, so this allows for at least as much secrecy
        # as before.
        # Use unbuffered appends because we don't want concurrent writes to get
        # spliced due to buffering.
        path = os.path.join(settings.VOTING_DIR, 'vote_record_%d' % topic.id)
        voting_record = open(path, 'a', 0)
        voting_record.write('%d | %s | %s | %s\n' %
                            (request.user.id, salt, vote_ids, key))
        voting_record.close()

        vote_values = "\n".join([unicode(o) for o in options])
        send_mail(from_email=settings.EMAIL_VOTING_FROM,
                  recipient_list=[request.user.email],
                  subject="GCD secret ballot receipt",
                  message=EMAIL_RECEIPT % (topic, vote_values,
                                           settings.EMAIL_VOTING_ADMIN,
                                           salt, vote_ids),
                  fail_silently=(not settings.BETA))

    return HttpResponseRedirect(urlresolvers.reverse('ballot',
      kwargs={ 'id': option.topic.id }))

def agenda(request, id):
    agenda = get_object_or_404(Agenda, id=id)

    # The "open" field on the topic object is somewhat misleading.
    # It means that the topic has been approved for an active ballot.
    # Ballots that are complete still have open=True, and ballots that were never
    # approved (much less completed) still have open=False.  This translates
    # the conditions into what you would expect for open or closed ballots.
    past_due = Q(deadline__lte=datetime.now())
    open = agenda.topics.exclude(past_due | Q(open=False))
    closed = agenda.topics.filter(past_due & Q(open=True))

    pending_items = agenda.items.filter(state__isnull=True)
    open_items = agenda.items.filter(state=True)

    _calculate_results(closed.filter(result_calculated=False))

    pending_topics, voted_topics, forbidden_topics = \
      _classify_topics(open.order_by('-deadline'), request.user)

    # result_counts = map(lambda t: (t.name, t.results().count()), closed)
    # raise Exception, result_counts
    return render_to_response('voting/agenda.html',
                              {
                                'agenda': agenda,
                                'closed_topics': closed.order_by('-deadline'),
                                'pending_topics': pending_topics,
                                'voted_topics': voted_topics,
                                'forbidden_topics': forbidden_topics,
                                'open_items': open_items,
                                'pending_items': pending_items,
                              },
                              context_instance=RequestContext(request))

