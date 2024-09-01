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
    path('doctor-change-password/',DoctorPasswordChangeView.as_view(),name="doctor-change-password")
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
