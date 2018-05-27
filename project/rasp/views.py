from django.shortcuts import render
from .models import Duty_setting, Users, Company, WeekendSetting, Skills_limits, Skill, Rating, DayResults, UserDayResults
from django.views.generic.edit import FormView
from .forms import DayResultForm
import datetime
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


class DayResultView(FormView):
    template_name = 'rasp/schedule.html'
    form_class = DayResultForm
    success_url = '/admin/rasp/dayresults/'
    def get(self, request, *args, **kwargs):
        on_duty = {}
        users_daysoff = {}
        skill_limit = {}
        days_all = Duty_setting.objects.all()
        users_all = Users.objects.all()
        skill_all = Skill.objects.all()
        rating = Rating.objects.all()
        for day in days_all:
            on_duty[day] = {}
            skill_limit[day] = {}
            skill_in_day = (day.skills_per_day.values_list(flat=True))
            for skill in skill_all:
                skill_limit[day][skill.nameSkill] = day.skills_per_day.values_list('sum_employee', flat=True).get(
                    pk=skill_in_day[skill.id - 1])
                on_duty[day][skill.nameSkill] = []
            for user in users_all:
                users_daysoff[user] = user.daysoff
                for skill_name in rating.filter(user=user).values_list('skill__nameSkill', flat=True):
                    if str(day.id) not in users_daysoff[user]:
                        if user not in on_duty[day][skill_name]:
                            on_duty[day][skill_name].append(user)

        def del_dublicate(day, skill_name):
            keys = on_duty[day].keys()
            del_key = 0
            for user in users_all:
                for key in keys:
                    if user in on_duty[day][key]:
                        del_key = del_key + 1
                        if skill_name == key and del_key > 1:
                            on_duty[day][key].remove(user)
                del_key = 0

        def change_skill(day, skill_name):
            keys = on_duty[day].keys()
            for key in keys:
                key != skill_name
                if len(on_duty[day][key]) > skill_limit[day][key]:
                    for user in on_duty[day][key]:
                        skillz = rating.values_list('skill', flat=True).filter(user=user)
                        if len(skillz) > 1:
                            on_duty[day][key].remove(user)
                            on_duty[day][skill_name].append(user)
                            return True
            return False

        def get_overlay(day, skill_name, skill_limit):
            on_duty_with_skill = len(on_duty[day][skill_name])
            if on_duty_with_skill > skill_limit[day][skill_name]:
                return on_duty[day][skill_name]
            return False

        def fill_one_user(cur_day, skill_name, skill_limit):
            finded_user = None
            user_ratings = rating.filter(skill__nameSkill=skill_name).order_by('value').values('user__id_user', 'value')
            user_settings_dict = {key['user__id_user']: key['value'] for key in user_ratings}
            for next_day in days_all:
                overlay_users = get_overlay(next_day, skill_name, skill_limit)
                if not overlay_users:
                    continue
                available_users = list(set(overlay_users) - set(on_duty[cur_day][skill_name]))
                if not len(available_users):
                    continue
                min_rate = 100
                for user in available_users:
                    keys = on_duty[cur_day].keys()
                    enum = 0
                    for key in keys:
                        if user not in on_duty[cur_day][key]:
                            enum += 1
                            if enum == len(keys):
                                if min_rate > user_settings_dict[
                                    users_all.filter(userName=user).values_list('id_user', flat=True)[0]]:
                                    min_rate = user_settings_dict[
                                        users_all.filter(userName=user).values_list('id_user', flat=True)[0]]
                                    finded_user = user
                break

            if finded_user:
                on_duty[cur_day][skill_name].append(finded_user)
                skill_names = rating.filter(user__userName=finded_user).values_list('skill__nameSkill', flat=True)
                if len(skill_names) > 1:
                    for user_skill_name in skill_names:
                        if finded_user in on_duty[next_day][user_skill_name]:
                            on_duty[next_day][user_skill_name].remove(finded_user)
                else:
                    on_duty[next_day][skill_name].remove(finded_user)
            else:
                for next_day in days_all:
                    if change_skill(next_day, skill_name):
                        fill_one_user(cur_day, skill_name, skill_limit)
                        break

        for day in days_all:
            for skill_per_day in day.skills_per_day.all():
                # print(skill_per_day)
                skill_name = skill_per_day.skill.nameSkill
                del_dublicate(day, skill_name)
                on_duty_with_skill = len(on_duty[day][skill_name])
                if on_duty_with_skill < skill_limit[day][skill_name]:
                    for count in range(skill_limit[day][skill_name] - on_duty_with_skill):
                        # print(day.id, skill_name, 'find')
                        fill_one_user(day, skill_name, skill_limit)

        context_data = self.get_context_data()
        context_data['res'] = on_duty

        return self.render_to_response(context_data)

    def post(self, request, *args, **kwargs):
        base_day = datetime.datetime.strptime(request.POST.get('base_day'), "%d-%m-%Y").date()
        for num, day in enumerate(Duty_setting.objects.all()):
            daydata = request.POST.getlist('daydata-%s' % day.day_name)
            cur_day = DayResults(date=base_day+datetime.timedelta(days=num), income=0, day_num=day.day_num)
            cur_day.save()
            for pair in daydata:
                data = pair.split(':')
                user = Users.objects.get(id_user=data[1])
                skill = Skill.objects.get(nameSkill=data[0])
                user_day_results = UserDayResults(user=user, skill=skill, day=cur_day)
                user_day_results.save()

        return super().post(request, *args, **kwargs)

def getRating(request):
    ratings = Rating.objects.all()
    return render(request, 'rasp/rating.html', {'ratings': ratings})





