# Generated by Django 2.0.4 on 2018-04-30 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='daysoff',
            name='weekendsPerWeek',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
