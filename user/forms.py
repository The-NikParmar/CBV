from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django import forms
from django.contrib.auth import authenticate


class CustomUserForm(UserCreationForm):
    class Meta:
        model  = CustomUser
        fields = ['first_name','last_name','phone_number','email','date_of_birth','age','address','gender','password1','password2']
        
class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data
    