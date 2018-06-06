from django.urls import path

from . import views

app_name = 'rasp'
urlpatterns = [
    path('daysoff/', views.daysoff, name='daysoff'),
    path('daysoff/vote/', views.vote, name='vote'),
    path('schedule/company', views.company, name='compa ny'),
    path('schedule/', views.DayResultView.as_view(), name='schedule'),
    path('stat/rating', views.getRating, name='rating'),
    path('stat/', views.stat, name='stat'),
    path('stat/income', views.income, name='income'),
    path('actual_schedule/', views.actual_schedule, name='actual_schedule'),
    path('stat/dynamic_rating', views.dynamic_rating, name='dynamic_rating'),
    path('pay/', views.pay, name='pay'),
    path('pay/payroll_preparation', views.payroll_preparation, name='payroll_preparation')
]