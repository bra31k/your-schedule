# my_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('rasp/', include('schedule.rasp.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
]
