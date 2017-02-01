# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0015_myfile__preview'),
    ]

    operations = [
        migrations.CreateModel(
            name='LivePhoto',
            fields=[
                ('photofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='files.PhotoFile')),
                ('video', models.OneToOneField(help_text='Link to the video file for the live part of the photo', on_delete=django.db.models.deletion.CASCADE, to='files.VideoFile')),
            ],
            bases=('files.photofile',),
        ),
        migrations.AddField(
            model_name='myfile',
            name='is_system',
            field=models.BooleanField(default=False, help_text='If file needs to be hidden'),
        ),
    ]
