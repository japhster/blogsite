# Generated by Django 2.1.3 on 2018-11-16 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0010_auto_20181116_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardset',
            name='card',
        ),
        migrations.AlterField(
            model_name='collector',
            name='collection',
            field=models.ManyToManyField(to='collector.Card'),
        ),
        migrations.DeleteModel(
            name='CardSet',
        ),
    ]