from django.urls import path

from . import views

app_name = 'rasp'
urlpatterns = [
    path('schedule/', views.schedule, name=""),
    path('schedule/daysoff/', views.daysoff, name='daysoff'),
    path('schedule/daysoff/vote/', views.vote, name='vote'),
    path('schedule/get_schedule/', views.DayResultView.as_view(), name='get_schedule'),
    path('schedule/actual_schedule/', views.actual_schedule, name='actual_schedule'),
    path('schedule/tardiness/', views.tardiness, name='tardiness'),
    path('stat/', views.stat, name='stat'),
    path('stat/rating', views.getRating, name='rating'),
    path('stat/income', views.income, name='income'),
    path('stat/dynamic_rating', views.dynamic_rating, name='dynamic_rating'),
    path('pay/', views.pay, name='pay'),
    path('pay/payroll_preparation', views.payroll_preparation, name='payroll_preparation')
]