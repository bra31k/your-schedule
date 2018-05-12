from django.shortcuts import render
from .models import DaysOff, PersonalVotes, Company, WeekendSetting
#from django.http import HttpResponseRedirect
#from .forms import PersonalVotesForm

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
#            PersonalVotes.selected_day = listObject[0] + listObject[1]
#            PersonalVotes.userName = request.user
            personal = PersonalVotes(selected_day=listObject[0] + listObject[1], userName=request.user)
            personal.save()
            selected_daysoff = DaysOff.objects.get(pk=listObject[1])
            return render(request, 'rasp/vote.html', {'daysoffs': selected_daysoff})

def shedule(request):
    employeeinday = 3
    weekends = []
    maxEmp = []
    minEmp = []
    selected_days = []
    name = []
    rasp = []
    i = 0
    emp = 0
    for item in WeekendSetting.objects.all():
        weekends.append(int(item.weekendsPerWeek))
    for item in PersonalVotes.objects.all():
        name.append(item.userName)
    for item in PersonalVotes.objects.all():
        selected_days.append([])
        for j in range(weekends[0]):
            selected_days[i].append(int(item.selected_day[j]))
        i=i+1
    for i in range(len(name)):
        rasp.append([])
        for j in range(7):
            rasp[i].append(j+1)
    for i in range(len(name)):
        for j in range(7):
            for k in range(weekends[0]):
                if selected_days[i][k] == rasp[i][j]:
                    rasp[i][j] = 0
    for j in range(7):
        for i in range(len(name)):
            if rasp[i][j] != 0:
                emp = emp + 1
        if emp > employeeinday:
            maxEmp.append(j+1)
            emp = 0
        elif emp < employeeinday:
            minEmp.append(j+1)
            emp = 0
        else:
            emp = 0
    return render(request, 'rasp/shedule.html', {'selected_days':  rasp})



