from django.urls import path

from . import views

app_name = 'rasp'
urlpatterns = [
    path('daysoff/', views.daysoff, name='daysoff'),
    path('daysoff/vote/', views.vote, name='vote'),
    path('schedule/company', views.company, name='compa ny'),
    path('schedule/', views.DayResultView.as_view(), name='schedule'),
    path('stat/rating', views.getRating, name='rating'),
    path('stat/', views.income, name='stat'),
    path('stat/income', views.income, name='income'),
]