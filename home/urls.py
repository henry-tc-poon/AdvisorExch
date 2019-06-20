from django.conf.urls import url
from django.urls import path
from . import views

app_name='home'

urlpatterns = [
    path('',              views.vHome,         name=''),
    path(r'',             views.vHome,         name='home'),
]
