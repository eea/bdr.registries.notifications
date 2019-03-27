# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-27 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_remove_unique_together_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='representative_country_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='representative_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='representative_vat',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
