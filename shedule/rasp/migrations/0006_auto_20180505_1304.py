# Generated by Django 2.0.4 on 2018-05-05 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasp', '0005_personalvotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weekendsetting',
            name='weekendsPerWeek',
            field=models.CharField(max_length=1),
        ),
    ]
