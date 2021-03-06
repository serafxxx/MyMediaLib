# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-06 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0010_auto_20160906_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='TagType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.TagType'),
        ),
        migrations.AddField(
            model_name='imprt',
            name='tags',
            field=models.ManyToManyField(to='files.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('type', 'value')]),
        ),
    ]
