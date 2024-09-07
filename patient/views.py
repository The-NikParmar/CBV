from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import AppointmentForm
from custom_admin.forms import PatientUpdateForm
from doctor.models import Doctor
from patient.models import Patient
from custom_admin.models import Disease
from django.http import JsonResponse
from django.utils import timezone
from patient.models import Appointment
from user.mixins import PatientLoginRequiredMixin
from datetime import datetime,timedelta
from user.models  import CustomUser
from .utils import calculate_available_slots

class UserDashboard(TemplateView):
    template_name = 'patient/user-index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, user=self.request.user)
        latest_appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')[:5]
        doctors = Doctor.objects.all()
        context['doctors'] = doctors
        context['latest_appointments'] = latest_appointments
        return context
    
class AppointmentsView(PatientLoginRequiredMixin,ListView):
    model = Appointment
    template_name = 'patient/appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(patient__user=self.request.user)
    
class BookAppointmentView(FormView):
    template_name = 'patient/book-appointment.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('patient:appointments')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        doctor_id = self.request.GET.get('doctor_id')
        if doctor_id:
            kwargs['initial'] = {'doctor': doctor_id}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = self.request.GET.get('doctor_id')
        doctors = Doctor.objects.all()
        context['doctors'] = doctors

        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                specialization = doctor.specialization
                diseases = Disease.objects.filter(specialization=specialization)
                context['diseases'] = diseases
            except Doctor.DoesNotExist:
                context['diseases'] = Disease.objects.none()
        
        return context

    def form_valid(self, form):
        user = self.request.user
        patient = get_object_or_404(Patient, user=user)
        appointment = form.save(commit=False)
        appointment.patient = patient
        appointment.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

def get_diseases(request):
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return JsonResponse({'error': 'Doctor ID not provided'}, status=400)
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        specialization = doctor.specialization
        diseases = Disease.objects.filter(specialization=specialization).values('id', 'problem_name', 'time_required')
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)
    return JsonResponse({'diseases': list(diseases)})

def get_available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    appointment_date = request.GET.get('appointment_date')
    disease_id = request.GET.get('disease_id')

    if not doctor_id or not appointment_date or not disease_id:
        return JsonResponse({'slots': [], 'error': 'Missing parameters'}, status=400)
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        disease = Disease.objects.get(id=disease_id)
        disease_duration = disease.time_required
    except Doctor.DoesNotExist:
        return JsonResponse({'slots': [], 'error': 'Doctor not found'}, status=404)
    except Disease.DoesNotExist:
        return JsonResponse({'slots': [], 'error': 'Disease not found'}, status=404)
    except Exception as e:
        return JsonResponse({'slots': [], 'error': str(e)}, status=500)

    appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    available_slots = calculate_available_slots(doctor, appointment_date, disease_duration)
    return JsonResponse({'slots': available_slots})

class PatientProfileView(PatientLoginRequiredMixin, TemplateView):
    template_name = 'patient/about-patient.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = Patient.objects.get(user=self.request.user)
        context['patient'] = patient
        context['appointments'] = Appointment.objects.filter(patient=patient)
        return context
    
class PatientEditView(PatientLoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = PatientUpdateForm
    template_name = 'patient/edit-patient.html'
    success_url = reverse_lazy('patient:patient-profile')
    
    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object()
        return kwargs

class DoctorsView(PatientLoginRequiredMixin,ListView):
    model = Doctor
    template_name = "patient/doctors.html"
    context_object_name = 'doctors'
    
    