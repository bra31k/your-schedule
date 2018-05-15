from django.shortcuts import render
from .models import DaysOff, PersonalVotes, Company, WeekendSetting, SkillPerDay
# from django.http import HttpResponseRedirect
# from .forms import PersonalVotesForm


def company(request):
    comps = Company.objects.all()
    return render(request, 'rasp/company.html', {'comps': comps})


def daysoff(request):
    daysoffs = DaysOff.objects.all()
    return render(request, 'rasp/daysoff.html', {'daysoffs': daysoffs})


def vote(request):
    if request.method == "POST":
        listObject = request.POST.getlist('daysoff[]')
        if len(listObject) == 3:
            personal = PersonalVotes(selected_day=listObject[0] + listObject[1], userName=request.user)
            personal.save()
            selected_daysoff = DaysOff.objects.get(pk=listObject[1])
            return render(request, 'rasp/vote.html', {'daysoffs': selected_daysoff})


def schedule(request):
    maxEmp = {}
    minEmp = {}
    selected_days = []
    name_list = []
    rasp = {}
    per_day_rasp = {}
    per_day_limits = DaysOff.objects.all()
    emp = 0
    sum_emp_in_day = []
    not_enough_people = False
    too_much_people = False
    weekends = range(int(WeekendSetting.objects.first().weekendsPerWeek))

    for num, item in enumerate(PersonalVotes.objects.all()):
        name_list.append(item.userName)
        selected_days.append([])
        for weekend_day in weekends:
            selected_days[num].append(int(item.selected_day[weekend_day]))
    name_count_range = range(len(name_list))

    for day in per_day_limits:
        sum_emp_in_day.append(sum(day.skills_per_day.values_list('employee_in_day', flat=True)))

    for day_num, day in enumerate(per_day_limits):
        rasp[day_num + 1] = {}
        maxEmp[day_num + 1] = False
        minEmp[day_num + 1] = False
        for name in name_count_range:
            is_workday = True
            for weekend_day in weekends:
                if selected_days[name][weekend_day] == day_num + 1:
                    is_workday = False

            if is_workday:
                emp = emp + 1
            rasp[day_num + 1][name] = is_workday
        if emp > sum_emp_in_day[day_num]:
            maxEmp[day_num + 1] = True
        elif emp < sum_emp_in_day[day_num]:
            minEmp[day_num + 1] = True
        emp = 0

    for day_num, day in enumerate(per_day_limits):
        actual_day = day_num + 1
        per_day_rasp[actual_day] = []
        for name in name_count_range:
            if rasp[actual_day][name]:
                per_day_rasp[actual_day].append(name)
        if minEmp[actual_day]:
            if sum(maxEmp.values()):
                for name in name_count_range:
                    if name in per_day_rasp[actual_day]:
                        continue
                    for max_day in maxEmp:
                        if sum(rasp[actual_day].values()) == sum_emp_in_day[actual_day - 1]:
                            minEmp[actual_day] = False
                            break
                        if rasp[max_day][name] and maxEmp[max_day] and name not in per_day_rasp[actual_day]:
                            per_day_rasp[actual_day].append(name)
                            if max_day in per_day_rasp:
                                per_day_rasp[max_day].remove(name)
                            rasp[max_day][name] = False
                            rasp[actual_day][name] = True
                            if sum(rasp[max_day].values()) <= sum_emp_in_day[max_day - 1]:
                                maxEmp[max_day] = False
    if sum(minEmp.values()):
        not_enough_people = True
    if sum(maxEmp.values()):
        too_much_people = True
    return render(request, 'rasp/schedule.html', {'too_much_people': too_much_people, 'not_enough_people': not_enough_people, 'res': per_day_rasp})
