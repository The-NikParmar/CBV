from django.db import models
from user.models import *
from django.db import models
from user.models import CustomUser  

class Specialization(models.Model):
    specialization_name = models.CharField(max_length=100)

    def __str__(self):
        return self.specialization_name
        
class Disease(models.Model):
    problem_name = models.CharField(max_length=100, unique=True)
    time_required = models.DurationField()  
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.problem_name} (Specialization: {self.specialization.specialization_name})"

class RoomAllotment(models.Model):
    ROOM_TYPES = [
        ('ICU', 'ICU'),
        ('General', 'General'),
        ('Private', 'Private'),
    ]
    
    room_type = models.CharField(max_length=30, choices=ROOM_TYPES)
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)  
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE) 
    allotment_date = models.DateField(null=True, blank=True)
    discharge_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.room_type}"
