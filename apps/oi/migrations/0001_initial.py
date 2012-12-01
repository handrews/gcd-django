# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('gcd', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'Changeset'
        db.create_table('oi_changeset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('indexer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changesets', to=orm['auth.User'])),
            ('approver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='approved_changeset', null=True, to=orm['auth.User'])),
            ('change_type', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('migrated', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('date_inferred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('imps', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('oi', ['Changeset'])

        # Adding M2M table for field along_with on 'Changeset'
        db.create_table('oi_changeset_along_with', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('changeset', models.ForeignKey(orm['oi.changeset'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('oi_changeset_along_with', ['changeset_id', 'user_id'])

        # Adding M2M table for field on_behalf_of on 'Changeset'
        db.create_table('oi_changeset_on_behalf_of', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('changeset', models.ForeignKey(orm['oi.changeset'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('oi_changeset_on_behalf_of', ['changeset_id', 'user_id'])

        # Adding model 'ChangesetComment'
        db.create_table('oi_changeset_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('commenter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['oi.Changeset'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('revision_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('old_state', self.gf('django.db.models.fields.IntegerField')()),
            ('new_state', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('oi', ['ChangesetComment'])

        # Adding model 'OngoingReservation'
        db.create_table('oi_ongoing_reservation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indexer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ongoing_reservations', to=orm['auth.User'])),
            ('series', self.gf('django.db.models.fields.related.OneToOneField')(related_name='ongoing_reservation', unique=True, to=orm['gcd.Series'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('oi', ['OngoingReservation'])

        # Adding M2M table for field along_with on 'OngoingReservation'
        db.create_table('oi_ongoing_reservation_along_with', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ongoingreservation', models.ForeignKey(orm['oi.ongoingreservation'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('oi_ongoing_reservation_along_with', ['ongoingreservation_id', 'user_id'])

        # Adding M2M table for field on_behalf_of on 'OngoingReservation'
        db.create_table('oi_ongoing_reservation_on_behalf_of', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ongoingreservation', models.ForeignKey(orm['oi.ongoingreservation'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('oi_ongoing_reservation_on_behalf_of', ['ongoingreservation_id', 'user_id'])

        # Adding model 'PublisherRevision'
        db.create_table('oi_publisher_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publisherrevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year_began', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_ended', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_began_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year_ended_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Publisher'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gcd.Country'])),
            ('is_master', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imprint_revisions', null=True, to=orm['gcd.Publisher'])),
            ('date_inferred', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('oi', ['PublisherRevision'])

        # Adding model 'IndiciaPublisherRevision'
        db.create_table('oi_indicia_publisher_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='indiciapublisherrevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year_began', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_ended', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_began_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year_ended_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('indicia_publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.IndiciaPublisher'])),
            ('is_surrogate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='indicia_publishers_revisions', to=orm['gcd.Country'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='indicia_publisher_revisions', null=True, to=orm['gcd.Publisher'])),
        ))
        db.send_create_signal('oi', ['IndiciaPublisherRevision'])

        # Adding model 'BrandRevision'
        db.create_table('oi_brand_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='brandrevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year_began', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_ended', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_began_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year_ended_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Brand'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='brand_revisions', null=True, to=orm['gcd.Publisher'])),
        ))
        db.send_create_signal('oi', ['BrandRevision'])

        # Adding model 'CoverRevision'
        db.create_table('oi_cover_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coverrevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('cover', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Cover'])),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cover_revisions', to=orm['gcd.Issue'])),
            ('marked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_replacement', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_wraparound', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('front_left', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('front_right', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('front_bottom', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('front_top', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('file_source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('oi', ['CoverRevision'])

        # Adding model 'SeriesRevision'
        db.create_table('oi_series_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seriesrevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Series'])),
            ('reservation_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('leading_article', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('year_began', self.gf('django.db.models.fields.IntegerField')()),
            ('year_ended', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_began_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year_ended_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_current', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publication_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tracking_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('has_barcode', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_indicia_frequency', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_isbn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_issue_title', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_volume', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_comics_publication', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='series_revisions', to=orm['gcd.Country'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='series_revisions', to=orm['gcd.Language'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='series_revisions', to=orm['gcd.Publisher'])),
            ('imprint', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='imprint_series_revisions', null=True, to=orm['gcd.Publisher'])),
            ('date_inferred', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('oi', ['SeriesRevision'])

        # Adding model 'IssueRevision'
        db.create_table('oi_issue_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issuerevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Issue'])),
            ('after', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='after_revisions', null=True, to=orm['gcd.Issue'])),
            ('revision_sort_code', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('reservation_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('no_title', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('volume', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('no_volume', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_volume_with_number', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('variant_of', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variant_revisions', null=True, to=orm['gcd.Issue'])),
            ('variant_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('key_date', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('year_on_sale', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('month_on_sale', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('day_on_sale', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('on_sale_date_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('indicia_frequency', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('no_indicia_frequency', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('price', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('page_count', self.gf('django.db.models.fields.DecimalField')(default=None, null=True, max_digits=10, decimal_places=3, blank=True)),
            ('page_count_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('editing', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('no_editing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issue_revisions', to=orm['gcd.Series'])),
            ('indicia_publisher', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='issue_revisions', null=True, blank=True, to=orm['gcd.IndiciaPublisher'])),
            ('indicia_pub_not_printed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='issue_revisions', null=True, blank=True, to=orm['gcd.Brand'])),
            ('no_brand', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isbn', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('no_isbn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('barcode', self.gf('django.db.models.fields.CharField')(default='', max_length=38, blank=True)),
            ('no_barcode', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_inferred', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('oi', ['IssueRevision'])

        # Adding model 'StoryRevision'
        db.create_table('oi_story_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='storyrevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Story'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('title_inferred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feature', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gcd.StoryType'])),
            ('sequence_number', self.gf('django.db.models.fields.IntegerField')()),
            ('page_count', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('page_count_uncertain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('script', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pencils', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('inks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('colors', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('letters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('editing', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('no_script', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_pencils', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_inks', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_colors', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_letters', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_editing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('job_number', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('genre', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('characters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('synopsis', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('reprint_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='story_revisions', null=True, to=orm['gcd.Issue'])),
            ('date_inferred', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('oi', ['StoryRevision'])

        # Adding model 'ReprintRevision'
        db.create_table('oi_reprint_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reprintrevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('reprint', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Reprint'])),
            ('reprint_from_issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.ReprintFromIssue'])),
            ('reprint_to_issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.ReprintToIssue'])),
            ('issue_reprint', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.IssueReprint'])),
            ('origin_story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='origin_reprint_revisions', null=True, to=orm['gcd.Story'])),
            ('origin_revision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='origin_reprint_revisions', null=True, to=orm['oi.StoryRevision'])),
            ('origin_issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='origin_reprint_revisions', null=True, to=orm['gcd.Issue'])),
            ('target_story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_reprint_revisions', null=True, to=orm['gcd.Story'])),
            ('target_revision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_reprint_revisions', null=True, to=orm['oi.StoryRevision'])),
            ('target_issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_reprint_revisions', null=True, to=orm['gcd.Issue'])),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', max_length=255)),
            ('in_type', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('out_type', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.OneToOneField')(related_name='next_revision', unique=True, null=True, to=orm['oi.ReprintRevision'])),
        ))
        db.send_create_signal('oi', ['ReprintRevision'])

        # Adding model 'Download'
        db.create_table('oi_download', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('oi', ['Download'])

        # Adding model 'ImageRevision'
        db.create_table('oi_image_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changeset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imagerevisions', to=orm['oi.Changeset'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['gcd.Image'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, db_index=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gcd.ImageType'])),
            ('image_file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('marked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_replacement', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('oi', ['ImageRevision'])


    def backwards(self, orm):
        # Deleting model 'Changeset'
        db.delete_table('oi_changeset')

        # Removing M2M table for field along_with on 'Changeset'
        db.delete_table('oi_changeset_along_with')

        # Removing M2M table for field on_behalf_of on 'Changeset'
        db.delete_table('oi_changeset_on_behalf_of')

        # Deleting model 'ChangesetComment'
        db.delete_table('oi_changeset_comment')

        # Deleting model 'OngoingReservation'
        db.delete_table('oi_ongoing_reservation')

        # Removing M2M table for field along_with on 'OngoingReservation'
        db.delete_table('oi_ongoing_reservation_along_with')

        # Removing M2M table for field on_behalf_of on 'OngoingReservation'
        db.delete_table('oi_ongoing_reservation_on_behalf_of')

        # Deleting model 'PublisherRevision'
        db.delete_table('oi_publisher_revision')

        # Deleting model 'IndiciaPublisherRevision'
        db.delete_table('oi_indicia_publisher_revision')

        # Deleting model 'BrandRevision'
        db.delete_table('oi_brand_revision')

        # Deleting model 'CoverRevision'
        db.delete_table('oi_cover_revision')

        # Deleting model 'SeriesRevision'
        db.delete_table('oi_series_revision')

        # Deleting model 'IssueRevision'
        db.delete_table('oi_issue_revision')

        # Deleting model 'StoryRevision'
        db.delete_table('oi_story_revision')

        # Deleting model 'ReprintRevision'
        db.delete_table('oi_reprint_revision')

        # Deleting model 'Download'
        db.delete_table('oi_download')

        # Deleting model 'ImageRevision'
        db.delete_table('oi_image_revision')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gcd.brand': {
            'Meta': {'ordering': "['name']", 'object_name': 'Brand'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Publisher']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'year_began': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'gcd.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'gcd.cover': {
            'Meta': {'ordering': "['issue']", 'object_name': 'Cover'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'front_bottom': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'front_left': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'front_right': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'front_top': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_wraparound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Issue']"}),
            'last_upload': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'limit_display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'gcd.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'marked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.ImageType']"})
        },
        'gcd.imagetype': {
            'Meta': {'object_name': 'ImageType', 'db_table': "'gcd_image_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'unique': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'gcd.indiciapublisher': {
            'Meta': {'ordering': "['name']", 'object_name': 'IndiciaPublisher', 'db_table': "'gcd_indicia_publisher'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_surrogate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'issue_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Publisher']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'year_began': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'gcd.issue': {
            'Meta': {'ordering': "['series', 'sort_code']", 'unique_together': "(('series', 'sort_code'),)", 'object_name': 'Issue'},
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '38', 'db_index': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Brand']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'display_volume_with_number': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'editing': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicia_frequency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'indicia_pub_not_printed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'indicia_publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.IndiciaPublisher']", 'null': 'True'}),
            'is_indexed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'key_date': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'no_barcode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_brand': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_editing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_indicia_frequency': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_isbn': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_title': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_volume': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'on_sale_date': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'on_sale_date_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page_count': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3'}),
            'page_count_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publication_date': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Series']"}),
            'sort_code': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'valid_isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'db_index': 'True'}),
            'variant_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'variant_of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variant_set'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'gcd.issuereprint': {
            'Meta': {'object_name': 'IssueReprint', 'db_table': "'gcd_issue_reprint'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'origin_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_issue_reprints'", 'to': "orm['gcd.Issue']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'target_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_issue_reprints'", 'to': "orm['gcd.Issue']"})
        },
        'gcd.language': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'gcd.publisher': {
            'Meta': {'ordering': "['name']", 'object_name': 'Publisher'},
            'brand_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imprint_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'indicia_publisher_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'is_master': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'issue_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imprint_set'", 'null': 'True', 'to': "orm['gcd.Publisher']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'series_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'year_began': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'gcd.reprint': {
            'Meta': {'object_name': 'Reprint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_reprints'", 'to': "orm['gcd.Story']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_reprints'", 'to': "orm['gcd.Story']"})
        },
        'gcd.reprintfromissue': {
            'Meta': {'object_name': 'ReprintFromIssue', 'db_table': "'gcd_reprint_from_issue'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'origin_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_reprints'", 'to': "orm['gcd.Issue']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_issue_reprints'", 'to': "orm['gcd.Story']"})
        },
        'gcd.reprinttoissue': {
            'Meta': {'object_name': 'ReprintToIssue', 'db_table': "'gcd_reprint_to_issue'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_issue_reprints'", 'to': "orm['gcd.Story']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'target_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_reprints'", 'to': "orm['gcd.Issue']"})
        },
        'gcd.series': {
            'Meta': {'ordering': "['sort_name', 'year_began']", 'object_name': 'Series'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'first_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_issue_series_set'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'has_barcode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_gallery': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'has_indicia_frequency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_isbn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_issue_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_volume': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imprint': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imprint_series_set'", 'null': 'True', 'to': "orm['gcd.Publisher']"}),
            'is_comics_publication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'issue_count': ('django.db.models.fields.IntegerField', [], {}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Language']"}),
            'last_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_issue_series_set'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'open_reserve': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'publication_dates': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publication_notes': ('django.db.models.fields.TextField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Publisher']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'sort_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'tracking_notes': ('django.db.models.fields.TextField', [], {}),
            'year_began': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gcd.story': {
            'Meta': {'ordering': "['sequence_number']", 'object_name': 'Story'},
            'characters': ('django.db.models.fields.TextField', [], {}),
            'colors': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'editing': ('django.db.models.fields.TextField', [], {}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inks': ('django.db.models.fields.TextField', [], {}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Issue']"}),
            'job_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'letters': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'no_colors': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_editing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_inks': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_letters': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_pencils': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'no_script': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'page_count': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'db_index': 'True'}),
            'page_count_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'pencils': ('django.db.models.fields.TextField', [], {}),
            'reprint_notes': ('django.db.models.fields.TextField', [], {}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'synopsis': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.StoryType']"})
        },
        'gcd.storytype': {
            'Meta': {'ordering': "['sort_code']", 'object_name': 'StoryType', 'db_table': "'gcd_story_type'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'sort_code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'oi.brandrevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'BrandRevision', 'db_table': "'oi_brand_revision'"},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Brand']"}),
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'brandrevisions'", 'to': "orm['oi.Changeset']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'brand_revisions'", 'null': 'True', 'to': "orm['gcd.Publisher']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'year_began': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'oi.changeset': {
            'Meta': {'object_name': 'Changeset'},
            'along_with': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'changesets_assisting'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'approver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'approved_changeset'", 'null': 'True', 'to': "orm['auth.User']"}),
            'change_type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imps': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'indexer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changesets'", 'to': "orm['auth.User']"}),
            'migrated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'on_behalf_of': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'changesets_source'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'state': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'oi.changesetcomment': {
            'Meta': {'ordering': "['created']", 'object_name': 'ChangesetComment', 'db_table': "'oi_changeset_comment'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['oi.Changeset']"}),
            'commenter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_state': ('django.db.models.fields.IntegerField', [], {}),
            'old_state': ('django.db.models.fields.IntegerField', [], {}),
            'revision_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'oi.coverrevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'CoverRevision', 'db_table': "'oi_cover_revision'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coverrevisions'", 'to': "orm['oi.Changeset']"}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Cover']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'file_source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'front_bottom': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'front_left': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'front_right': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'front_top': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_replacement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_wraparound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cover_revisions'", 'to': "orm['gcd.Issue']"}),
            'marked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'oi.download': {
            'Meta': {'object_name': 'Download'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oi.imagerevision': {
            'Meta': {'ordering': "['created']", 'object_name': 'ImageRevision', 'db_table': "'oi_image_revision'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagerevisions'", 'to': "orm['oi.Changeset']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Image']"}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_replacement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.ImageType']"})
        },
        'oi.indiciapublisherrevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'IndiciaPublisherRevision', 'db_table': "'oi_indicia_publisher_revision'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indiciapublisherrevisions'", 'to': "orm['oi.Changeset']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indicia_publishers_revisions'", 'to': "orm['gcd.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicia_publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.IndiciaPublisher']"}),
            'is_surrogate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'indicia_publisher_revisions'", 'null': 'True', 'to': "orm['gcd.Publisher']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'year_began': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'oi.issuerevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'IssueRevision', 'db_table': "'oi_issue_revision'"},
            'after': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'after_revisions'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'barcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '38', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'issue_revisions'", 'null': 'True', 'blank': 'True', 'to': "orm['gcd.Brand']"}),
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issuerevisions'", 'to': "orm['oi.Changeset']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'day_on_sale': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'display_volume_with_number': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editing': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicia_frequency': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'indicia_pub_not_printed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'indicia_publisher': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'issue_revisions'", 'null': 'True', 'blank': 'True', 'to': "orm['gcd.IndiciaPublisher']"}),
            'isbn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'key_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'month_on_sale': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'no_barcode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_brand': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_editing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_indicia_frequency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_isbn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_volume': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'on_sale_date_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page_count': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'page_count_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'reservation_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'revision_sort_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issue_revisions'", 'to': "orm['gcd.Series']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'variant_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'variant_of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variant_revisions'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'volume': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'year_on_sale': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'oi.ongoingreservation': {
            'Meta': {'object_name': 'OngoingReservation', 'db_table': "'oi_ongoing_reservation'"},
            'along_with': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ongoing_assisting'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ongoing_reservations'", 'to': "orm['auth.User']"}),
            'on_behalf_of': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ongoing_source'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'series': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ongoing_reservation'", 'unique': 'True', 'to': "orm['gcd.Series']"})
        },
        'oi.publisherrevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'PublisherRevision', 'db_table': "'oi_publisher_revision'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publisherrevisions'", 'to': "orm['oi.Changeset']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_master': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imprint_revisions'", 'null': 'True', 'to': "orm['gcd.Publisher']"}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Publisher']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'year_began': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'oi.reprintrevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'ReprintRevision', 'db_table': "'oi_reprint_revision'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reprintrevisions'", 'to': "orm['oi.Changeset']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'issue_reprint': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.IssueReprint']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255'}),
            'origin_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin_reprint_revisions'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'origin_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin_reprint_revisions'", 'null': 'True', 'to': "orm['oi.StoryRevision']"}),
            'origin_story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin_reprint_revisions'", 'null': 'True', 'to': "orm['gcd.Story']"}),
            'out_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'previous_revision': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'next_revision'", 'unique': 'True', 'null': 'True', 'to': "orm['oi.ReprintRevision']"}),
            'reprint': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Reprint']"}),
            'reprint_from_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.ReprintFromIssue']"}),
            'reprint_to_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.ReprintToIssue']"}),
            'target_issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target_reprint_revisions'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'target_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target_reprint_revisions'", 'null': 'True', 'to': "orm['oi.StoryRevision']"}),
            'target_story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target_reprint_revisions'", 'null': 'True', 'to': "orm['gcd.Story']"})
        },
        'oi.seriesrevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'SeriesRevision', 'db_table': "'oi_series_revision'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seriesrevisions'", 'to': "orm['oi.Changeset']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series_revisions'", 'to': "orm['gcd.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'has_barcode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_indicia_frequency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_isbn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_issue_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_volume': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imprint': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imprint_series_revisions'", 'null': 'True', 'to': "orm['gcd.Publisher']"}),
            'is_comics_publication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series_revisions'", 'to': "orm['gcd.Language']"}),
            'leading_article': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'publication_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series_revisions'", 'to': "orm['gcd.Publisher']"}),
            'reservation_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Series']"}),
            'tracking_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'year_began': ('django.db.models.fields.IntegerField', [], {}),
            'year_began_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_ended': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_ended_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'oi.storyrevision': {
            'Meta': {'ordering': "['-created', '-id']", 'object_name': 'StoryRevision', 'db_table': "'oi_story_revision'"},
            'changeset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'storyrevisions'", 'to': "orm['oi.Changeset']"}),
            'characters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'colors': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'editing': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_revisions'", 'null': 'True', 'to': "orm['gcd.Issue']"}),
            'job_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'letters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'no_colors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_editing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_inks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_letters': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_pencils': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_script': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_count': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'page_count_uncertain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pencils': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reprint_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'null': 'True', 'to': "orm['gcd.Story']"}),
            'synopsis': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title_inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcd.StoryType']"})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['oi']
