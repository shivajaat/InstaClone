# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 08:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0013_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='post',
        ),
        migrations.DeleteModel(
            name='tags',
        ),
    ]