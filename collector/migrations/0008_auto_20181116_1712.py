# Generated by Django 2.1.3 on 2018-11-16 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0007_card_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copies', models.IntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.Card')),
            ],
        ),
        migrations.AlterField(
            model_name='collector',
            name='collection',
            field=models.ManyToManyField(to='collector.Copies'),
        ),
    ]
