# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20160830_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myfile',
            name='hash',
            field=models.CharField(db_index=True, max_length=64),
        ),
    ]
