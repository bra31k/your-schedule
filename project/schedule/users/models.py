from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    daysoff = models.CharField(max_length=7, null=True, blank=True, verbose_name='Выходные')
    days_worked = models.IntegerField(default=0, verbose_name='Отработанные дни')
    precentage = models.IntegerField(default=0, verbose_name='Процент от продаж')
    sum_precentage = models.IntegerField(default=0, verbose_name='Сумма процетных выплат', editable=False)
    salary = models.IntegerField(default=0, null=True, verbose_name='Оклад')
    tardiness = models.IntegerField(default=0, verbose_name='Прогулы')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username
