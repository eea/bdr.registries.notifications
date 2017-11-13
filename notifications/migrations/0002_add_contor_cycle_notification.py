# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-16 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cyclenotification',
            name='counter',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='person',
            name='company',
            field=models.ManyToManyField(related_name='user', to='notifications.Company'),
        ),
    ]
