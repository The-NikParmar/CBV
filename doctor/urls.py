from django.contrib import admin
from django.urls import path 
from doctor.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'doctor'

urlpatterns = [
    path('dashboard',DoctorDashboard.as_view(),name='dashboard'),
    path('doctor-profile',DoctorProfileView.as_view(),name='doctor-profile'),
    path('doctor-profile/edit/',EditProfileView.as_view(),name='edit-profile'),
    path('doctor-appointments/',DoctorAppointmentView.as_view(),name="doctor-appointments"),
    path('appointment/<int:pk>/approve/', AppointmentApproveView.as_view(), name='approve-appointment'),
    path('appointment/<int:pk>/reject/', AppointmentRejectView.as_view(), name='reject-appointment'), 
    path('doctor-patient',DoctorpatientView.as_view(),name='doctor-patient'),
    path('patient-detail/<int:pk>/', DoctorPatientDetailView.as_view(), name='patient-detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
