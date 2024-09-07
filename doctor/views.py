from django.shortcuts import render,get_object_or_404,redirect
from user.mixins import DoctorLoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from custom_admin.forms  import *
from patient.models import Appointment

class DoctorDashboard(DoctorLoginRequiredMixin,TemplateView):
    template_name = 'doctor/doctor_index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor, user=self.request.user)
        appointments = Appointment.objects.filter(doctor=doctor)
        total_patients = appointments.values('patient').distinct().count()
        approved_appointments_count = appointments.filter(status='C').count()
        rejected_appointments_count = appointments.filter(status='X').count()
        
        context['appointments'] = appointments
        context['total_patients'] = total_patients
        context['total_appointments'] = appointments.count()
        context['approved_appointments_count'] = approved_appointments_count
        context['rejected_appointments_count'] = rejected_appointments_count
        return context
    
class DoctorProfileView(DoctorLoginRequiredMixin,DetailView):
    model = Doctor
    template_name = 'doctor/doctor-profile.html'
    context_object_name = 'doctor'

    def get_object(self):
        return self.model.objects.get(user=self.request.user)
    
class EditProfileView(DoctorLoginRequiredMixin, UpdateView):
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

class DoctorAppointmentView(DoctorLoginRequiredMixin, ListView):
    template_name = 'doctor/appointments.html'
    model = Appointment
    
    def get_queryset(self):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        return Appointment.objects.filter(doctor=doctor)
    
class AppointmentApproveView(DoctorLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=self.kwargs['pk'])
        appointment.status = 'C'  
        appointment.save()
        return redirect('doctor:doctor-appointments')  

class AppointmentRejectView(DoctorLoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=self.kwargs['pk'])
        appointment.status = 'X'  
        appointment.save()
        return redirect('doctor:doctor-appointments')  
    
class DoctorpatientView(DoctorLoginRequiredMixin,TemplateView):
    template_name = 'doctor/doctor-patients.html'
    model = Appointment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor, user=self.request.user)
        appointments = Appointment.objects.filter(doctor=doctor)
        print(appointments)
        context['appointments'] = appointments
        return context
    
class DoctorPatientDetailView(DoctorLoginRequiredMixin,DetailView):
    template_name = 'doctor/about-patient.html'
    model = Appointment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor, user=self.request.user)
        appointment = self.get_object()
        patient = appointment.patient
        patient_appointments = Appointment.objects.filter(
            patient=patient, doctor=doctor
        ).select_related('doctor', 'disease')

        context['patient'] = patient
        context['patient_appointments'] = patient_appointments
        context['doctor'] = doctor
        return context
    