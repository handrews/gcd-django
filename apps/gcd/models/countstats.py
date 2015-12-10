# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from apps.gcd.models.publisher import Publisher, Brand, IndiciaPublisher
from apps.gcd.models.language import Language
from apps.gcd.models.country import Country
from apps.gcd.models.series import Series
from apps.gcd.models.issue import Issue, INDEXED
from apps.gcd.models.story import Story
from apps.gcd.models.cover import Cover


class CountStatsManager(models.Manager):

    def init_stats(self, language=None, country=None):
        if language and country:
            raise ValueError('either country or language stats')
        self.filter(language=language, country=country).delete()
        if country:
            kwargs = {'country': country, 'deleted': False}
        else:
            kwargs = {'deleted': False}

        if language is None:
            self.create(name='publishers', country=country,
              count=Publisher.objects.filter(**kwargs).count())
            if not country:
                self.create(name='brands',
                  count=Brand.objects.filter(**kwargs).count())
            self.create(name='indicia publishers', country=country,
              count=IndiciaPublisher.objects.filter(**kwargs).count())
        else:
            kwargs['language'] = language

        self.create(name='series', language=language, country=country,
          count=Series.objects.filter(is_comics_publication=True,
                                      **kwargs).count())
        if 'language' in kwargs:
            kwargs['series__language'] = kwargs['language']
            kwargs.pop('language')
        if 'country' in kwargs:
            kwargs['series__country'] = kwargs['country']
            kwargs.pop('country')
        kwargs['series__is_comics_publication'] = True

        self.create(name='issues', language=language, country=country,
          count=Issue.objects.filter(variant_of=None, **kwargs).count())

        self.create(name='variant issues', language=language, country=country,
          count=Issue.objects.filter(**kwargs)\
                                     .exclude(variant_of=None).count())

        self.create(name='issue indexes', language=language, country=country,
          count=Issue.objects.filter(variant_of=None, **kwargs)\
                     .exclude(is_indexed=INDEXED['skeleton']).count())

        if 'series__language' in kwargs:
            kwargs['issue__series__language'] = kwargs['series__language']
            kwargs.pop('series__language')
        if 'series__country' in kwargs:
            kwargs['issue__series__country'] = kwargs['series__country']
            kwargs.pop('series__country')
        kwargs.pop('series__is_comics_publication')

        self.create(name='covers', language=language, country=country,
          count=Cover.objects.filter(**kwargs).count())

        self.create(name='stories', language=language, country=country,
          count=Story.objects.filter(**kwargs).count())

    def update_count(self, field, delta, language=None, country=None):
        """
        Updates a single statistic (generic, per language, and per country).

        The generic statistic is always updated.  The language and/or
        country statistics are updated if their respective parameters
        are not None.
        """
        stat = self.get(name=field, language=None, country=None)
        stat.count = models.F('count') + delta
        stat.save()

        if language:
            try:
                stat = self.get(name=field, language=language, country=None)
                stat.count = models.F('count') + delta
                stat.save()
            except CountStats.DoesNotExist:
                self.init_stats(language=language)

        if country:
            try:
                stat = self.get(name=field, language=None, country=country)
                stat.count = models.F('count') + delta
                stat.save()
            except CountStats.DoesNotExist:
                self.init_stats(country=country)

    def update_all_counts(self, deltas, negate=False,
                          language=None, country=None):
        """
        Apply the deltas to the various statistices.

        Language and country can both be updated at once.
        The generic stats (with language and country both None) are always
        updated.  If neither language nor country are passed, then only
        the generic stats are updated.

        By default, the deltas are added, but if negate=True, then the
        deltas will be subtracted (by negating them before update).

        If the language or country do not have stats yet, they will
        be initialized and the deltas will not be applied to them.
        As this should be called after the changes have been committed
        back to the display (which is needed to get the deltas),
        the stats initialization will include the latest changes.
        """
        if country and not self.filter(country=country,
                                       language=None).exists():
            self.init_stats(country=country)
            country = None

        if language and not self.filter(language=language,
                                        country=None).exists():
            self.init_stats(language=language)
            language = None

        for field in deltas:
            delta = -deltas[field] if negate else deltas[field]
            self.update_count(field=field, delta=delta,
                              language=language, country=country)


class CountStats(models.Model):
    """
    Store stats from gcd database.
    """
    class Meta:
        app_label = 'gcd'
        db_table = 'gcd_count_stats'

    class Admin:
        pass

    objects = CountStatsManager()

    name = models.CharField(max_length=40, db_index=True)
    count = models.IntegerField()
    language = models.ForeignKey(Language, null=True)
    country = models.ForeignKey(Country, null=True)

    def __unicode__(self):
        return self.name + ": " + str(self.count)
