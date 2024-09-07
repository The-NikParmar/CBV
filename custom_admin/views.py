from django.views.generic import * 
from custom_admin.forms import *
import sweetify
from django.urls import reverse_lazy
from user.models import CustomUser
from  django.contrib.auth.mixins import LoginRequiredMixin
from user.mixins import AdminLoginRequiredMixin


class DashboardView(AdminLoginRequiredMixin,TemplateView):
    template_name = "custom_admin/index.html"
    
class SpecializationView(AdminLoginRequiredMixin,ListView):
    template_name = "custom_admin/specialization.html"
    context_object_name = 'specializations'
    model = Specialization
    
class SpecializationAddView(AdminLoginRequiredMixin,CreateView):
    model = Specialization
    fields = ['specialization_name']
    template_name = 'custom_admin/add-specialization.html'
    success_url = reverse_lazy('custom-admin:specialization')  
    
    def form_valid(self, form):
        response = super().form_valid(form)
        sweetify.success(self.request, 'Specialization added successfully!')
        return response    
    
class SpecializationUpdateView(AdminLoginRequiredMixin,UpdateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'custom_admin/edit-specialization.html'
    success_url = reverse_lazy('custom-admin:specialization')  
    
    def form_valid(self, form):
        response = super().form_valid(form)
        sweetify.success(self.request, 'Specialization updated successfully!')
        return response

class SpecializationDeleteView(AdminLoginRequiredMixin,DeleteView):
    model = Specialization
    success_url = reverse_lazy('custom-admin:specialization')
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        sweetify.success(self.request, 'Specialization deleted successfully!')
        return response
                  
class DoctorsView(AdminLoginRequiredMixin,ListView):
    model = Doctor
    template_name = "custom_admin/doctors.html"
    context_object_name = 'doctors'
    
class AddDoctorView(AdminLoginRequiredMixin,CreateView):
    model = CustomUser
    form_class = CustomUserDoctorForm
    template_name = "custom_admin/add-doctor.html"
    success_url = reverse_lazy('custom-admin:doctors')  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        print("Form Errors:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
    
class EditDoctorView(AdminLoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorUpdateForm
    template_name = "custom_admin/edit-doctor.html"  
    success_url = reverse_lazy('custom-admin:doctors') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        print("Form Errors:", form.errors)
        return self.render_to_response(self.get_contextd_data(form=form))
       
class DeleteDoctorView(AdminLoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'custom_admin/confirm_delete.html'
    success_url = reverse_lazy('custom-admin:doctors')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'custom_admin/about-doctor.html'  
    context_object_name = 'doctor'
    
class RoomListView(ListView):
    model = RoomAllotment
    template_name = 'custom_admin/rooms.html'
    context_object_name = 'rooms'
    
class ADDRoomView(AdminLoginRequiredMixin,CreateView):
    model = RoomAllotment
    form_class = RoomAllotmentForm
    template_name = "custom_admin/add-room.html"
    success_url = reverse_lazy('custom-admin:rooms')  
    
class DeleteRoomView(DeleteView):
    model = RoomAllotment
    template_name = 'custom_admin/rooms.html'
    success_url = reverse_lazy('custom-admin:rooms')
    
class UpdateRoomView(AdminLoginRequiredMixin,UpdateView):
    model = RoomAllotment
    form_class = RoomAllotmentForm
    template_name = 'custom_admin/edit-room.html'
    success_url = reverse_lazy('custom-admin:rooms')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = CustomUser.objects.filter(role=CustomUser.Patient)
        context['doctors'] = CustomUser.objects.filter(role=CustomUser.Doctor)
        return context
    
class PatientListView(AdminLoginRequiredMixin,ListView):
    model = Patient
    template_name = 'custom_admin/patients.html'
    context_object_name = 'patients'
    
class PatientDetailView(AdminLoginRequiredMixin,DetailView):
    model = Patient
    template_name = 'custom_admin/about-patient.html'
    context_object_name = 'patient'
    
class PatientUpdateView(AdminLoginRequiredMixin,UpdateView):
    model = Patient
    form_class = PatientUpdateForm
    template_name = 'custom_admin/edit-patient.html'
    success_url = reverse_lazy('custom-admin:patients') 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user  
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
class DeletePatientView(AdminLoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'custom_admin/confirm_delete.html'
    success_url = reverse_lazy('custom-admin:patients')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class AppointmentsListView(AdminLoginRequiredMixin, TemplateView):
    template_name = "custom_admin/appointments.html"
    
    
class DiseaseView(AdminLoginRequiredMixin,ListView):
    template_name = "custom_admin/disease.html"
    context_object_name = 'diseases'
    model = Disease
    
class DiseaseAddView(AdminLoginRequiredMixin, CreateView):
    model = Disease
    form_class = DiseaseForm
    template_name ="custom_admin/add-disease.html"
    success_url = reverse_lazy('custom-admin:doctors') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        return context
    
class DiseaseUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = Disease
    form_class = DiseaseForm
    template_name = "custom_admin/edit-disease.html"
    success_url = reverse_lazy('custom-admin:disease')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        return context

class DiseaseDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = Disease
    template_name = "custom_admin/disease.html"
    success_url = reverse_lazy('custom-admin:disease')