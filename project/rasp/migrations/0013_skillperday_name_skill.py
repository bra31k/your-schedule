# Generated by Django 2.0.5 on 2018-05-14 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rasp', '0012_auto_20180514_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillperday',
            name='name_skill',
            field=models.CharField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rasp.Skill'), max_length=30),
        ),
    ]