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
    users_all = Users.objects.all()
#    print(Users.objects.all().values_list('skill', flat=True))
    for day in days_all:
        on_duty[day.id] = {}
        skill_limit[day.id] = {}
        skill_in_day = (day.skills_per_day.values_list(flat=True))
        for skill in Skill.objects.all():
            skill_limit[day.id][skill.id] = day.skills_per_day.values_list('sum_employee', flat=True).get(pk=skill_in_day[skill.id-1])
            on_duty[day.id][skill.id] = []
        for user in users_all:
            users_daysoff[user.id_user] = user.daysoff
            skills = user.skills.values_list('id', flat = True)
            for id in range(len(skills)):
                if str(day.day_num) not in users_daysoff[user.id_user]:
                    if user.id_user not in on_duty[day.id][skills[id]]:
                        on_duty[day.id][skills[id]].append(user.id_user)

    print(on_duty)
    def del_dublicate(day, skill_id):
        keys = on_duty[day].keys()
        del_key = 0
        for user in users_all:
            for key in keys:
                if user.id in on_duty[day][key]:
                    del_key = del_key + 1
                    if skill_id == key and del_key > 1:
                        on_duty[day][key].remove(user.id)
            del_key = 0

    def change_skill(day_id, skill_id):
        keys = on_duty[day.id].keys()
        for key in keys:
            key != skill_id
            if len(on_duty[day_id][key]) > skill_limit[day_id][key]:
                for id_user in on_duty[day_id][key]:
                    skillz = users_all.values_list('skills', flat=True).filter(id_user=id_user)
                    if len(skillz) > 1:
                        on_duty[day_id][key].remove(id_user)
                        on_duty[day_id][skill_id].append(id_user)
                        return True
        return False


    def get_overlay(day_id, skill_id, skill_limit):
        on_duty_with_skill = len(on_duty[day_id][skill_id])
        if on_duty_with_skill > skill_limit[day_id][skill_id]:
            return on_duty[day_id][skill_id]
        return False

    def fill_one_user(cur_day, skill_id, skill_limit):
        finded_user = None
        for next_day in days_all[cur_day:]:
            overlay_users = get_overlay(next_day.id, skill_id, skill_limit)
            if not overlay_users:
                # not found enough people for this skill at this day
                continue
            available_users = list(set(overlay_users) - set(on_duty[cur_day][skill_id]))
            if not len(available_users):
                continue
            for user in range(len(available_users)):
                if available_users[user] not in on_duty[cur_day]:
                    finded_user = available_users[user]
            break


        if finded_user:
            on_duty[cur_day][skill_id].append(finded_user)
            on_duty[next_day.id][skill_id].remove(finded_user)
        else:
            for next_day in days_all[cur_day:]:
                if change_skill(next_day.id, skill_id):
                    fill_one_user(cur_day, skill_id, skill_limit)

    for day in days_all:
        skill_in_day = (day.skills_per_day.values_list(flat=True))
        skill_id = day.skills_per_day.values_list('skill', flat=True)
        for id in range(len(skill_in_day)):
            del_dublicate(day.id, skill_id[id])
            on_duty_with_skill = len(on_duty[day.id][skill_id[id]])
            if on_duty_with_skill < skill_limit[day.id][skill_id[id]]:
                for count in range(skill_limit[day.id][skill_id[id]] - on_duty_with_skill):
                    print(day.id, skill_id[id])
                    fill_one_user(day.id, skill_id[id], skill_limit)


    print(on_duty)

    return render(request, 'rasp/schedule.html', {'res': on_duty})






