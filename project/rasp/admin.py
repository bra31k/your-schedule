from django.contrib import admin

from .models import Duty_setting, WeekendSetting, Users, Company, Skill, Skills_limits, Rating

admin.site.register(Duty_setting)
admin.site.register(WeekendSetting)
admin.site.register(Users)
admin.site.register(Company)
admin.site.register(Skill)
admin.site.register(Skills_limits)
admin.site.register(Rating)