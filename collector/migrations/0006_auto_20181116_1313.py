# Generated by Django 2.1.3 on 2018-11-16 13:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0005_auto_20181115_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='collector',
            name='coins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='collector',
            name='last_collected_coins',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='latest collection'),
        ),
    ]
