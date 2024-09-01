from django.contrib import admin
from django.urls import path 
from patient.views import *

app_name = 'patient'

urlpatterns = [
    path('user_index',UserDashboard.as_view(),name='user_index'),
    
    path('appointments',AppointmentsView.as_view(),name='appointments'),
    path('book-appointment',BookAppointmentView.as_view(),name='book-appointment'),
    path('get-diseases/', get_diseases, name='get_diseases'),
]
