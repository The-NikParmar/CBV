# forms.py
from django import forms
from .models import Appointment
from django.core.exceptions import ValidationError
from custom_admin.models import Disease
from doctor.models import Doctor
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'disease', 'appointment_date', 'appointment_time']

    def __init__(self, *args, **kwargs):
        doctor_id = kwargs.pop('doctor_id', None)
        super().__init__(*args, **kwargs)

        self.fields['doctor'].queryset = Doctor.objects.all()

        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                specialization = doctor.specialization
                self.fields['disease'].queryset = Disease.objects.filter(specialization=specialization)
                self.fields['doctor'].initial = doctor_id
            except Doctor.DoesNotExist:
                self.fields['disease'].queryset = Disease.objects.none()
        
    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        duration = cleaned_data.get('duration', timedelta(minutes=30))

        if doctor and appointment_date and appointment_time:
            appointment_start = timezone.datetime.combine(appointment_date, appointment_time)
            appointment_end = appointment_start + duration

            # Check for overlapping appointments
            overlapping_appointments = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date
            ).filter(
                appointment_time__lt=appointment_end.time(),  # Existing appointment ends after new appointment starts
                appointment_time__gt=appointment_start.time()   # Existing appointment starts before new appointment ends
            )

            if overlapping_appointments.exists():
                raise forms.ValidationError('The doctor already has an appointment at this time.')

        return cleaned_data
    