from django.urls import path

from . import views

app_name = 'rasp'
urlpatterns = [
    path('daysoff/', views.daysoff, name='daysoff'),
    path('shedule/vote/', views.vote, name='vote'),
    path('', views.company, name='company'),
    path('shedule/', views.shedule, name='shedule')
]