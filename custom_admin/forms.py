from django import forms
from custom_admin.models import Specialization, RoomAllotment, Disease
from django.utils.crypto import get_random_string
from user.models import CustomUser
from doctor.models import Doctor
from patient.models import Patient
from .task import send_welcome_email


class SpecializationForm(forms.ModelForm):
    
    class Meta:
        model = Specialization
        fields = ['specialization_name']
        
        
class CustomUserDoctorForm(forms.ModelForm):
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), required=True)
    experience = forms.IntegerField(required=True)
    doctor_details = forms.CharField(max_length=200, required=True)
    profile_photo = forms.ImageField(required=False) 
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender', 'address', 'age']
    
    def save(self, commit=True):
        password = get_random_string(length=8)  
        
        user = super().save(commit=False)
        user.set_password(password)
        print(password) # Tempory Password 
        user.role = CustomUser.Doctor
        
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                experience=self.cleaned_data['experience'],
                doctor_details=self.cleaned_data['doctor_details'],
                profile_photo=self.cleaned_data['profile_photo']
            ) 
            
            # Celery task to send email
            send_welcome_email.delay(user.email, password)
        return user

  
class DoctorUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=False)
    address = forms.CharField(max_length=255, required=False)
    age = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), required=False)
    experience = forms.IntegerField(required=True)
    doctor_details = forms.CharField(max_length=200, required=True)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = Doctor
        fields = ['specialization', 'experience', 'doctor_details', 'profile_photo']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['phone_number'].initial = self.user.phone_number
            self.fields['date_of_birth'].initial = self.user.date_of_birth
            self.fields['gender'].initial = self.user.gender
            self.fields['address'].initial = self.user.address
            self.fields['age'].initial = self.user.age
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


    def save(self, commit=True):
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.phone_number = self.cleaned_data['phone_number']
            self.user.date_of_birth = self.cleaned_data['date_of_birth']
            self.user.gender = self.cleaned_data['gender']
            self.user.address = self.cleaned_data['address']
            self.user.age = self.cleaned_data['age']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        doctor = super().save(commit=False)
        if commit:
            doctor.save()
        
        return doctor
    
class RoomAllotmentForm(forms.ModelForm):

    class Meta:
        model = RoomAllotment
        fields = ['room_type', 'patient', 'doctor','allotment_date','discharge_date']
        widgets = {
            'allotment_date': forms.DateInput(attrs={'type': 'date'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth', 'gender', 'address', 'age', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone_number'].initial = user.phone_number
            self.fields['date_of_birth'].initial = user.date_of_birth
            self.fields['gender'].initial = user.gender
            self.fields['address'].initial = user.address
            self.fields['age'].initial = user.age
            self.fields['email'].initial = user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = self.user
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.phone_number = self.cleaned_data['phone_number']
            user.date_of_birth = self.cleaned_data['date_of_birth']
            user.gender = self.cleaned_data['gender']
            user.address = self.cleaned_data['address']
            user.age = self.cleaned_data['age']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
        return user
    
class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['problem_name', 'time_required', 'specialization']

    problem_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Disease Name'})
    )
    time_required = forms.DurationField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter in seconds'})
    )
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
