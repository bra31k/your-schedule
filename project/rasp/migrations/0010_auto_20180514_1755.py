# Generated by Django 2.0.5 on 2018-05-14 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rasp', '0009_auto_20180514_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillPerDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_in_day', models.IntegerField()),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rasp.Skill')),
            ],
        ),
        migrations.RemoveField(
            model_name='daysoff',
            name='employeeInDay',
        ),
        migrations.AddField(
            model_name='daysoff',
            name='skills_per_day',
            field=models.ManyToManyField(to='rasp.SkillPerDay'),
        ),
    ]