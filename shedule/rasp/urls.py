from django.urls import path

from . import views

app_name = 'rasp'
urlpatterns = [
    path('shedule/', views.shedule, name='shedule'),
    path('shedule/vote/', views.vote, name='vote'),
    path('', views.company, name='company')
]