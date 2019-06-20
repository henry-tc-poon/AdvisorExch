from django.conf.urls import url
from django.urls import path
from . import views

app_name='advisorInfo'

urlpatterns = [
    path(r'',                      views.vAdvisor,         name='advisor'),
    path(r'advisor',               views.vAdvisor,         name='advisor'),
    path(r'demographic',           views.vDemographic,     name='demographic'),
    path(r'composition',           views.vComposition,     name='composition'),
    path(r'clientInfo',            views.vClientInfo,      name='clientInfo'),
    path(r'revenue',               views.vRevenue,         name='revenue'),
    path(r'investment',            views.vInvestment,      name='investment'),
    path(r'serviceProvided',       views.vService,         name='service'),
    path(r'logout',                views.vLogout,          name='logout'),
]
