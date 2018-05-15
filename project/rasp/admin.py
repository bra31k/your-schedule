from django.contrib import admin

from .models import DaysOff, WeekendSetting, PersonalVotes, Company, Skill, SkillPerDay

admin.site.register(DaysOff)
admin.site.register(WeekendSetting)
admin.site.register(PersonalVotes)
admin.site.register(Company)
admin.site.register(Skill)
admin.site.register(SkillPerDay)