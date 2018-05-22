from django.shortcuts import render
from .models import Duty_setting, Users, Company, WeekendSetting, Skills_limits, Skill
# from django.http import HttpResponseRedirect
# from .forms import PersonalVotesForm


def company(request):
    comps = Company.objects.all()
    return render(request, 'rasp/company.html', {'comps': comps})


def daysoff(request):
    daysoffs = Duty_setting.objects.all()
    return render(request, 'rasp/daysoff.html', {'daysoffs': daysoffs})


def vote(request):
    if request.method == "POST":
        listObject = request.POST.getlist('daysoff[]')
        if len(listObject) == 3:
            personal = Users(selected_day=listObject[0] + listObject[1], userName=request.user)
            personal.save()
            selected_daysoff = Duty_setting.objects.get(pk=listObject[1])
            return render(request, 'rasp/vote.html', {'daysoffs': selected_daysoff})



def schedule(request):
    on_duty = {}
    users_daysoff = {}
    skill_limit = {}
    days_all = Duty_setting.objects.all()
    for day in days_all:
        on_duty[day.id] = {}
        skill_limit[day.id] = {}
        skill_in_day = (day.skills_per_day.values_list(flat=True))
        for skill in Skill.objects.all():
            skill_limit[day.id][skill.id] = day.skills_per_day.values_list('sum_employee', flat=True).get(pk=skill_in_day[skill.id-1])
            on_duty[day.id][skill.id] = []
        for user in Users.objects.all():
            users_daysoff[user.id_user] = user.daysoff
            if str(day.day_num) not in users_daysoff[user.id_user]:
                if user.id_user not in on_duty[day.id][user.skills.id]:
                    on_duty[day.id][user.skills.id].append(user.id_user)
    print(skill_limit)


    def get_overlay(day_id, skill_id, skill_limit):
        on_duty_with_skill = len(on_duty[day_id][skill_id])
        if on_duty_with_skill > skill_limit[day_id][skill_id]:
            return on_duty[day_id][skill_id]
        return False

    def fill_one_user(cur_day, skill_id, skill_limit):
        finded_user = None
        for next_day in days_all[cur_day:]:
            overlay_users = get_overlay(next_day.id, skill_id, skill_limit)
#            print(overlay_users)
            if not overlay_users:
                # not found enough people for this skill at this day
                continue
            available_users = list(set(overlay_users) - set(on_duty[cur_day][skill_id]))
            if not len(available_users):
                continue
            for user in range(len(available_users)):
                if available_users[user] not in on_duty[cur_day][skill_id]:
                    finded_user = available_users[user]
            break

        if finded_user:
            on_duty[cur_day][skill_id].append(finded_user)
            on_duty[next_day.id][skill_id].remove(finded_user)

    for day in days_all:
        skill_in_day = (day.skills_per_day.values_list(flat=True))
        skill_id = day.skills_per_day.values_list('skill', flat=True)
        for id in range(len(skill_in_day)):
#            skill_limit = day.skills_per_day.values_list('sum_employee', flat=True).get(pk=skill_in_day[id])
#            print(skill_limit)
            on_duty_with_skill = len(on_duty[day.id][skill_id[id]])
#            print(on_duty_with_skill, skill_limit, day.id, skill_id[id])
            if on_duty_with_skill < skill_limit[day.id][skill_id[id]]:
                    for count in range(skill_limit[day.id][skill_id[id]] - on_duty_with_skill):
                        fill_one_user(day.id, skill_id[id], skill_limit)
                        print(day.id , skill_id[id], skill_limit[day.id][skill_id[id]])


    print(on_duty)

    return render(request, 'rasp/schedule.html', {'res': on_duty})






