# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-30 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180530_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('librarian', 'LIBRARIAN'), ('student', 'STUDENT')], default='student', max_length=50),
        ),
    ]
