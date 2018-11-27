# Generated by Django 2.1.3 on 2018-11-15 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0004_collector_join_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='owned_by',
        ),
        migrations.AddField(
            model_name='collector',
            name='collection',
            field=models.ManyToManyField(to='collector.Card'),
        ),
    ]
