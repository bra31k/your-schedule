from django.shortcuts import render
from .models import DaysOff, WeekendSetting, PersonalVotes
from django.http import HttpResponseRedirect
#from .forms import PersonalVotesForm


def shedule(request):
    daysoffs = DaysOff.objects.all()
    return render(request, 'rasp/shedule.html', {'daysoffs': daysoffs})

def vote(request):
    if request.method == "POST":
        listObject = request.POST.getlist('daysoff[]')
        if len(listObject) == 2:
#            PersonalVotes.selected_day = listObject[0] + listObject[1]
#            PersonalVotes.userName = request.user
            personal = PersonalVotes(selected_day=listObject[0] + listObject[1], userName=request.user)
            personal.save()
            selected_daysoff = DaysOff.objects.get(pk=listObject[1])
            return render(request, 'rasp/vote.html', {'daysoffs': selected_daysoff})
# Create your views here.
