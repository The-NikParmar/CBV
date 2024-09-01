from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from user.models import  CustomUser

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')
