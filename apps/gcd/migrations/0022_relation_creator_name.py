# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-14 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gcd', '0021_given_family_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorrelation',
            name='creator_name',
            field=models.ManyToManyField(related_name='creator_relation', to='gcd.CreatorNameDetail'),
        ),
    ]
