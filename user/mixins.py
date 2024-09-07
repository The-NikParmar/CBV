from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

class PatientLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('user:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        allowed_user_types = ['Patient']
        if request.user.role not in allowed_user_types:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

class DoctorLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('user:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        allowed_user_types = ['Doctor']
        if request.user.role not in allowed_user_types:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

class AdminLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('user:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        allowed_user_types = ['Admin']
        if request.user.role not in allowed_user_types:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

