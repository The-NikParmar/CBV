from django.urls import path 
from custom_admin.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'custom_admin'

urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    
    path('specialization/',SpecializationView.as_view(),name='specialization'),
    path('Addspecialization/',SpecializationAddView.as_view(),name='Addspecialization'),
    path('edit_specialization/<int:pk>/', SpecializationUpdateView.as_view(), name='edit_specialization'),
    path('delete_specialization/<int:pk>/', SpecializationDeleteView.as_view(), name='delete_specialization'),

    path('doctors/',DoctorsView.as_view(),name='doctors'),
    path('doctor/add/',AddDoctorView.as_view(),name='Adddoctor'),
    path('doctor/edit/<int:pk>/',EditDoctorView.as_view(),name='editdoctor'),
    path('doctor/delete/<int:pk>/', DeleteDoctorView.as_view(), name='delete-doctor'),
    path('doctor/about/<int:pk>',DoctorDetailView.as_view(), name='doctor-about'),
    
    path('rooms/',RoomListView.as_view(),name='rooms'),
    path('rooms/add',ADDRoomView.as_view(),name='Addrooms'),
    path('rooms/edit/<int:pk>/',UpdateRoomView.as_view(),name='edit-room'),
    path('rooms/delete/<int:pk>/',DeleteRoomView.as_view(),name='delete-room'),    
    
    path('patients/',PatientListView.as_view(),name='patients'),
    path('patients/about/<int:pk>',PatientDetailView.as_view(), name='patient-about'),
    path('patients/edit/<int:pk>', PatientUpdateView.as_view(), name='edit-patient'),
    path('patients/delete/<int:pk>/', DeletePatientView.as_view(), name='delete-patient'),

    path('appointments/',AppointmentsListView.as_view(),name='appointments'),
    
     path('disease/',DiseaseListView.as_view(),name='disease'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)