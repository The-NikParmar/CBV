from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.views.generic import * 
from .models import *   
from .forms import *
from patient.models import * 
from django.urls import reverse_lazy
from patient.views import *
from patient.urls import *
from doctor.urls import *

class PatientSignup(FormView):
    template_name = "user/sign-up.html"
    form_class = CustomUserForm
    
    def form_valid(self, form):
        form_class=self.form_class(self.request.POST)
        if form_class.is_valid():
            user=form_class.save(commit=False)
            user.save()
            patient = Patient(user=user)  
            patient.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
        
    def get_success_url(self):
        return reverse_lazy('user:login')
    
class CustomLoginView(FormView):
    form_class = EmailLoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('patient:user_index')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(self.request, user)
            if user.role == CustomUser.Patient:
                return redirect('patient:user_index')
            elif user.role == CustomUser.Doctor:
                return redirect('doctor:dashboard')
            elif user.role == CustomUser.Admin:
                return redirect('custom_admin:dashboard')  
            else:
                return redirect('patient:user_index')  
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form Errors:", form.errors)
        return super().form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request) 
        return redirect('user:login')  
    
    
    
