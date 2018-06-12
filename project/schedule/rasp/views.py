from django.shortcuts import render
from .models import Duty_setting, Users, WeekendSetting, Skill, Rating, DayResults, UserDayResults
from django.views.generic.edit import FormView
from .forms import DayResultForm
import datetime


def daysoff(request):

    daysoffs = Duty_setting.objects.all()

    return render(request, 'rasp/daysoff.html', {'daysoffs': daysoffs})


def manualDaysoff(request):

    if request.method == "POST":

        username = request.POST.get('user')
        listObject = request.POST.getlist('daysoff[]')
        user = Users.objects.get(username=username)
        weekends = WeekendSetting.objects.all()
        list_days_off = ''
        if len(listObject) == weekends.values_list('weekendsPerWeek', flat=True).get():
            for days in listObject:
                list_days_off += days
            user.daysoff = list_days_off
            user.save()

            return render(request, 'rasp/manual_daysoff.html')

    users = Users.objects.filter(daysoff__isnull=True)
    daysoffs = Duty_setting.objects.all()

    return render(request, 'rasp/manual_daysoff.html', {'users': users, 'daysoffs': daysoffs})


def vote(request):
    if request.method == "POST":
        listObject = request.POST.getlist('daysoff[]')
        weekends = WeekendSetting.objects.all()
        list_days_off = ''
        if len(listObject) == weekends.values_list('weekendsPerWeek', flat=True).get():
            for days in listObject:
                list_days_off += days
            request.user.daysoff = list_days_off
            request.user.save()
            return render(request, 'rasp/vote.html', {'daysoffs': list_days_off})


class DayResultView(FormView):
    template_name = 'rasp/get_schedule.html'
    form_class = DayResultForm
    success_url = '/admin/rasp/dayresults/'

    def get(self, request, *args, **kwargs):

        check = False

        for user in Users.objects.all():
            if len(user.daysoff) == 0:
                check = True

        on_duty = {}
        users_daysoff = {}
        skill_limit = {}
        days_all = Duty_setting.objects.all()
        users_all = Users.objects.all()
        skill_all = Skill.objects.all()
        rating = Rating.objects.all()
        dayz = []
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

        def change_skill(day, cur_day, skill_name, skill_limit):
            keys = on_duty[day].keys()
            for key in keys:
                key != skill_name
                if len(on_duty[day][key]) > skill_limit[day][key]:
                    for user in on_duty[day][key]:
                        skillz = rating.values_list('skill', flat=True).filter(user=user)
                        if len(skillz) > 1:
                            on_duty[day][key].remove(user)
                            on_duty[day][skill_name].append(user)
                            fill_one_user(cur_day, skill_name, skill_limit)
                            break

        def get_overlay(day, skill_name, skill_limit):
            on_duty_with_skill = len(on_duty[day][skill_name])
            if on_duty_with_skill > skill_limit[day][skill_name]:
                return on_duty[day][skill_name]
            return False

        def fill_one_user(cur_day, skill_name, skill_limit):
            finded_user = None
            user_ratings = rating.filter(skill__nameSkill=skill_name).order_by('value').values('user__id', 'value')
            user_settings_dict = {key['user__id']: key['value'] for key in user_ratings}
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
                                    users_all.filter(username=user).values_list('id', flat=True)[0]]:
                                    min_rate = user_settings_dict[
                                        users_all.filter(username=user).values_list('id', flat=True)[0]]
                                    finded_user = user
                break

            if finded_user:
                on_duty[cur_day][skill_name].append(finded_user)
                skill_names = rating.filter(user__username=finded_user).values_list('skill__nameSkill', flat=True)
                if len(skill_names) > 1:
                    for user_skill_name in skill_names:
                        if finded_user in on_duty[next_day][user_skill_name]:
                            on_duty[next_day][user_skill_name].remove(finded_user)
                else:
                    on_duty[next_day][skill_name].remove(finded_user)
            else:
                for next_day in days_all:
                    change_skill(next_day, cur_day, skill_name, skill_limit)





        for day in days_all:
            for skill_per_day in day.skills_per_day.all():
                skill_name = skill_per_day.skill.nameSkill
                del_dublicate(day, skill_name)
                on_duty_with_skill = len(on_duty[day][skill_name])
                if on_duty_with_skill < skill_limit[day][skill_name]:
                    for count in range(skill_limit[day][skill_name] - on_duty_with_skill):
                        fill_one_user(day, skill_name, skill_limit)

        context_data = self.get_context_data()
        context_data['res'] = on_duty

        return self.render_to_response(context_data)

    def post(self, request, *args, **kwargs):
        base_day = datetime.datetime.strptime(request.POST.get('base_day'), "%d-%m-%Y").date()
        for num, day in enumerate(Duty_setting.objects.all()):
            daydata = request.POST.getlist('daydata-%s' % day.day_name)
            if DayResults.objects.filter(date=base_day+datetime.timedelta(days=num)).exists():
                continue
            cur_day = DayResults(date=base_day+datetime.timedelta(days=num), income=0, day_num=day.day_num)
            cur_day.save()
            for pair in daydata:
                data = pair.split(':')
                user = Users.objects.get(id=data[1])
                skill = Skill.objects.get(nameSkill=data[0])
                user_day_results = UserDayResults(user=user, skill=skill, day=cur_day)
                user_day_results.save()

        return super().post(request, *args, **kwargs)


def createUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        Users.objects.create_user(username=username, email=email, password=password)
        return render(request, 'rasp/create_user.html', {'id': Users.objects.get(username=username).id})

    return render(request, 'rasp/create_user.html')


def getRating(request):
    has_permission = not request.user.is_anonymous
    ratings = Rating.objects.order_by('-value').all()
    opts = Rating._meta
    return render(request, 'rasp/rating.html', {'ratings': ratings, 'has_permission' : has_permission, 'opts' : opts})


def income(request):
    if request.method == "POST":
        date_start = datetime.datetime.strptime(request.POST.get('date_start'), "%Y-%m-%d").date()
        date_final = datetime.datetime.strptime(request.POST.get('date_final'), "%Y-%m-%d").date()
        income_data = []
        date = []
        day_results = []
        for num in range(DayResults.objects.get(date=date_final).id - DayResults.objects.get(date=date_start).id + 1):
            day_results.append(DayResults.objects.get(date=date_start+datetime.timedelta(days=num)))
        for day in day_results:
            income_data.append(str(day.income))
            date.append(str(day.date))

        return render(request, 'rasp/income.html', {'income_data': ','.join(income_data), 'x_labels': date})


def stat(request):

    dates = []
    for day in DayResults.objects.all():
        dates.append(str(day.date))

    users = []
    for user in Users.objects.all():
        users.append(user)

    return render(request, 'rasp/stat.html', {'dates': dates, 'users': users})


def actual_schedule(request):

    date = datetime.datetime.date(datetime.datetime.now())

    if DayResults.objects.filter(date=date).exists():
        monday = date - datetime.timedelta(days=date.weekday())
        sunday = monday + datetime.timedelta(days=6)
        day_results = DayResults.objects.filter(date__gte=monday, date__lte= sunday)

    return render(request, 'rasp/actual_schedule.html', {'day_results': day_results})


def schedule(request):
    return render(request, 'rasp/schedule.html')


def tardiness(request):
    dates = []
    for day in DayResults.objects.all():
        dates.append(str(day.date))

    users = []
    for user in Users.objects.all():
        users.append(user)

    user_is_finded = False

    if request.method == "POST":
        username = request.POST.get('user')
        date = datetime.datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()
        if UserDayResults.objects.filter(user__username=username, day__date=date).exists():
            skill = UserDayResults.objects.filter(user__username=username, day__date=date).values_list('skill', flat=True)
            change_rating = UserDayResults.objects.get(user__username=username, day__date=date)
            change_rating.change_point_rating -= 0.5
            change_rating.save()
            rating = Rating.objects.get(user__username=username, skill = skill[0])
            rating.value -= 0.5
            rating.save()
            user_is_finded = True
            user = Users.objects.get(username=username)
            user.tardiness = +1
            user.save()
            return render(request, 'rasp/tardiness.html', {'user_is_finded': user_is_finded})
        else:
            return render(request, 'rasp/tardiness.html', {'user_is_finded': user_is_finded, 'dates': dates, 'users': users})

    return render(request, 'rasp/tardiness.html', {'dates': dates, 'users': users})


def dynamic_rating(request):

    if request.method == "POST":
        rates = []
        dates = []
        username = request.POST.get('user')
        changes_rating = UserDayResults.objects.filter(user__username=username)

        for num, rate in enumerate(changes_rating):
            rates.append(round(rate.change_point_rating,1))
            dates.append(rate.day)


        change = 0
        for num in range(len(rates)):
            rates[num] = change + rates[num]
            change = rates[num]

        print(str(rates))

        return render(request, 'rasp/dynamic_rating.html', {'rates': str(rates), 'dates': dates})


def pay(request):
    dates = []
    for day in DayResults.objects.all():
        dates.append(str(day.date))

    users = []
    for user in Users.objects.all():
        users.append(user)

    return render(request, 'rasp/pay.html', {'dates': dates, 'users': users})


def payroll_preparation(request):
    if request.method == "POST":
        username = request.POST.get('user')
        date_start = datetime.datetime.strptime(request.POST.get('date_start'), "%Y-%m-%d").date()
        date_final = datetime.datetime.strptime(request.POST.get('date_final'), "%Y-%m-%d").date()
        user = Users.objects.get(username=username)
        day_results = []
        for num in range(DayResults.objects.get(date=date_final).id - DayResults.objects.get(date=date_start).id + 1):
            if DayResults.objects.filter(date=date_start + datetime.timedelta(days=num),userdayresults__user__username=username, userdayresults__pay = True):
                day_results.append(DayResults.objects.get(date=date_start + datetime.timedelta(days=num)))
        payroll = (user.salary/((7-len(user.daysoff))*4))*len(day_results)
        for day_result in day_results:
            payroll += (day_result.income/100 * user.precentage)
        payroll = round(payroll, 2)
        payroll_with_coefficient = round(payroll + 1.15, 3)
        real_payroll = round(payroll_with_coefficient/100 * 77, 3)
        days_worked = len(day_results)
        return render(request, 'rasp/payroll_preparation.html', {'payroll': payroll, 'payroll_with_coefficient': payroll_with_coefficient, 'real_payroll': real_payroll, 'days_worked': days_worked})





