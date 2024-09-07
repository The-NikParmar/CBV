from django.contrib import admin
from .models import *

admin.site.register(Patient)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor','appointment_date','appointment_time','end_time','disease')
