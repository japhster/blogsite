# Generated by Django 2.1.3 on 2018-11-12 17:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20181112_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='join_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='join date'),
        ),
    ]