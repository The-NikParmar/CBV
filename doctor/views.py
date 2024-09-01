from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from custom_admin.forms  import *
from .forms import ChangePasswordForm


# Create your views here.
class DoctorDashboard(TemplateView):
    template_name = 'doctor/doctor_index.html'
    
class DoctorProfileView(LoginRequiredMixin,DetailView):
    model = Doctor
    template_name = 'doctor/doctor-profile.html'
    context_object_name = 'doctor'

    def get_object(self):
        return self.model.objects.get(user=self.request.user)
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorUpdateForm
    template_name = "doctor/edit-doctor.html"  
    success_url = reverse_lazy('doctor:doctor-profile') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        return context

    def get_object(self):
        return self.model.objects.get(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DoctorPasswordChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('user:login')
    template_name = 'doctor/change_password.html'