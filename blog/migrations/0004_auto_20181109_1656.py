# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-09 16:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 16, 56, 38, 780908, tzinfo=utc), verbose_name='date published'),
        ),
    ]
