from django.contrib import admin

from .models import Duty_setting, WeekendSetting, Users, Skill, Skills_limits, DayResults, UserDayResults

admin.site.register(Duty_setting)
admin.site.register(WeekendSetting)
admin.site.register(Users)
admin.site.register(Skill)
admin.site.register(Skills_limits)
admin.site.register(DayResults)
admin.site.register(UserDayResults)