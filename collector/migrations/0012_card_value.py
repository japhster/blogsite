# Generated by Django 2.1.3 on 2018-11-16 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0011_auto_20181116_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='value',
            field=models.IntegerField(default=100),
        ),
    ]