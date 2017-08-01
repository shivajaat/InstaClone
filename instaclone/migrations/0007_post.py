# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0006_auto_20170724_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to=b'user_images')),
                ('img_url', models.CharField(max_length=200)),
                ('caption', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instaclone.UserModel')),
            ],
        ),
    ]
