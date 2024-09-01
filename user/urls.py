from django.contrib import admin
from django.urls import path 
from user.views import *

app_name = 'user'

urlpatterns = [
    path('', PatientSignup.as_view(), name='PatientSignup'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout')
]
