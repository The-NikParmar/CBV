from django.contrib import admin
from django.urls import path 
from patient.views import *

app_name = 'patient'

urlpatterns = [
    path('user-index',UserDashboard.as_view(),name='user_index'),
    
    path('appointments',AppointmentsView.as_view(),name='appointments'),
    path('book-appointment',BookAppointmentView.as_view(),name='book-appointment'),
    path('get-diseases/', get_diseases, name='get_diseases'),
    path('get_available_slots/', get_available_slots, name='get_available_slots'),
    path('patient-profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('patient-profile/edit/',PatientEditView.as_view(),name='edit-profile'),
    path('all-doctors/',DoctorsView.as_view(),name='all-doctors')
    
]
