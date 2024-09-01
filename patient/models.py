from django.db import models
from user.models import CustomUser, BaseModel
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class Patient(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

class Appointment(BaseModel):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('D', 'Completed'),
        ('X', 'Canceled'),
    ]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P') 
    patient =  models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE)
    disease = models.ForeignKey('custom_admin.Disease', on_delete=models.CASCADE)  
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_time:
            # Calculate end time based on appointment_time and disease duration
            start_datetime = datetime.combine(self.appointment_date, self.appointment_time)
            end_datetime = start_datetime + self.disease.time_required
            self.end_time = end_datetime.time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with Dr.  {self.doctor} for {self.patient} on {self.appointment_date} at {self.appointment_time}"

