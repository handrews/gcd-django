# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-04 19:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stddata', '0002_initial_data'),
        ('gcd', '0017_feature'),
        ('oi', '0016_cleanup_award_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureLogoRevision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('committed', models.NullBooleanField(db_index=True, default=None)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('leading_article', models.BooleanField(default=False)),
                ('year_began', models.IntegerField(blank=True, db_index=True, null=True)),
                ('year_ended', models.IntegerField(blank=True, null=True)),
                ('year_began_uncertain', models.BooleanField(default=False)),
                ('year_ended_uncertain', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('changeset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='featurelogorevisions', to='oi.Changeset')),
                ('feature', models.ManyToManyField(related_name='logo_revisions', to='gcd.Feature')),
                ('feature_logo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='revisions', to='gcd.FeatureLogo')),
                ('previous_revision', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_revision', to='oi.FeatureLogoRevision')),
            ],
            options={
                'ordering': ['-created', '-id'],
                'db_table': 'oi_feature_logo_revision',
            },
        ),
        migrations.CreateModel(
            name='FeatureRevision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('committed', models.NullBooleanField(db_index=True, default=None)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('leading_article', models.BooleanField(default=False)),
                ('genre', models.CharField(max_length=255)),
                ('year_created', models.IntegerField(blank=True, db_index=True, null=True)),
                ('year_created_uncertain', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('keywords', models.TextField(blank=True, default=b'')),
                ('changeset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='featurerevisions', to='oi.Changeset')),
                ('feature', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='revisions', to='gcd.Feature')),
                ('feature_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcd.FeatureType')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stddata.Language')),
                ('previous_revision', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_revision', to='oi.FeatureRevision')),
            ],
            options={
                'ordering': ['-created', '-id'],
                'db_table': 'oi_feature_revision',
            },
        ),
    ]
