from django.shortcuts import render
from .models import DaysOff, PersonalVotes, Company, WeekendSetting
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
           # PersonalVotes.selected_day = listObject[0] + listObject[1]
           # PersonalVotes.userName = request.user
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
    weekends = range(int(WeekendSetting.objects.first().weekendsPerWeek))

    for num, item in enumerate(PersonalVotes.objects.all()):
        name_list.append(item.userName)
        selected_days.append([])
        for weekend_day in weekends:
            selected_days[num].append(int(item.selected_day[weekend_day]))
    name_count_range = range(len(name_list))

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
        if emp > day.employeeInDay:
            maxEmp[day_num + 1] = True
        elif emp < day.employeeInDay:
            minEmp[day_num + 1] = True
        emp = 0

    for day_num, day in enumerate(per_day_limits):
        actual_day = day_num + 1
        per_day_rasp[actual_day] = []
        for name in name_count_range:
            if rasp[actual_day][name]:
                per_day_rasp[actual_day].append(name)
        if minEmp[actual_day]:
            got_worker = False
            max_to_shrink = False
            if sum(maxEmp.values()):
                for name in name_count_range:
                    if name in per_day_rasp[actual_day]:
                        continue
                    for max_day in maxEmp:
                        if rasp[max_day][name] and maxEmp[max_day]:
                            got_worker = True
                            per_day_rasp[actual_day].append(name)
                            rasp[max_day][name] = False
                            max_to_shrink = max_day
                            break
                    if got_worker:
                        if sum(rasp[max_day].values()) <= day.employeeInDay:
                            maxEmp[max_to_shrink] = False
                        break
            pass
        elif maxEmp[actual_day]:
            pass

    return render(request, 'rasp/schedule.html', {'rasp':  rasp, 'min_emp': minEmp, 'max_emp': maxEmp, 'res': per_day_rasp})
