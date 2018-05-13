from django.contrib import admin

from .models import DaysOff, WeekendSetting, PersonalVotes, Company

admin.site.register(DaysOff)
admin.site.register(WeekendSetting)
admin.site.register(PersonalVotes)
admin.site.register(Company)