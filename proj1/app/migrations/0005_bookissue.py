# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-12 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_user_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BookName', models.CharField(max_length=50)),
                ('StudentName', models.CharField(max_length=50)),
                ('BookStatus', models.CharField(choices=[('booked', 'BOOKED'), ('pickedUp', 'PICKED_UP'), ('returned', 'RETURNED')], default='returned', max_length=50)),
                ('ReturnDate', models.DateField(null=True)),
            ],
        ),
    ]