from django.db import models
from user.models import CustomUser, BaseModel
from custom_admin.models import Specialization

class Doctor(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    experience = models.IntegerField()
    doctor_details = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} || {self.specialization.specialization_name}"

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)
