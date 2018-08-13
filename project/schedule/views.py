from django.shortcuts import render
from schedule.rasp.models import DayResults
import datetime

def start_page(request):

    date = datetime.datetime.date(datetime.datetime.now())

    if DayResults.objects.filter(date=date).exists():
        monday = date - datetime.timedelta(days=date.weekday())
        sunday = monday + datetime.timedelta(days=6)
        day_results = DayResults.objects.filter(date__gte=monday, date__lte= sunday)

    return render(request, 'base.html', {'day_results': day_results})