from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import AppointmentForm
from doctor.models import Doctor
from patient.models import Patient
from custom_admin.models import Disease
from django.http import JsonResponse
from django.utils import timezone
from patient.models import Appointment
from datetime import datetime, timedelta




class UserDashboard(TemplateView):
    template_name = 'patient/user-index.html'
        
class AppointmentsView(TemplateView):
    template_name = 'patient/appointments.html'
    
class BookAppointmentView(FormView):
    template_name = 'patient/book-appointment.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('patient:appointments')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        doctor_id = self.request.GET.get('doctor_id')
        if doctor_id:
            kwargs['doctor_id'] = doctor_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        return context

    # def form_valid(self, form):
    #     try:
    #         user = self.request.user
    #         patient = get_object_or_404(Patient, user=user)
    #         appointment = form.save(commit=False)
    #         appointment.patient = patient
    #         appointment.save()
    #         return super().form_valid(form)
    #     except ValidationError as e:
    #         form.add_error(None, e.message) 
    #         return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        patient = get_object_or_404(Patient, user=user)
        appointment = form.save(commit=False)
        appointment.patient = patient
        
        # Get appointment details
        appointment_date = appointment.appointment_date
        appointment_time = appointment.appointment_time
        disease = appointment.disease
        doctor = appointment.doctor
        
        # Calculate start and end time based on disease duration
        start_datetime = timezone.make_aware(datetime.combine(appointment_date, appointment_time))
        end_datetime = start_datetime + disease.time_required
        
        # Check for overlapping appointments
        overlapping_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time__lt=end_datetime.time(),  # Appointments ending after the new start time
            end_time__gte=appointment_time             # Appointments starting before the new end time
        )
        
        if overlapping_appointments.exists():
            # Error message return karo agar slot book ho chuka hai
            form.add_error(None, "This time slot is already booked.")
            return self.form_invalid(form)
        
        # Appointment save karo agar slot available hai
        appointment.save()
        return super().form_valid(form)

    
    def form_invalid(self, form):
        print("Form errors:", form.errors)
        context = self.get_context_data(form=form)
        return self.render_to_response(self.get_context_data(form=form))
    
def get_diseases(request):
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return JsonResponse({'error': 'Doctor ID not provided'}, status=400)
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        specialization = doctor.specialization
        diseases = Disease.objects.filter(specialization=specialization).values('id', 'problem_name')
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)
    return JsonResponse({'diseases': list(diseases)})