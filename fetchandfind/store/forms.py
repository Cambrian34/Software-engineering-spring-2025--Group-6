from django import forms
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


from .models import User  # Custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2', 'user_role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user_role' field for regular users
        if not self.instance.is_superuser:
            self.fields['user_role'].widget = forms.HiddenInput()  # Hide field for non-admin users
            self.fields['user_role'].initial = 'customer'  # Default to 'customer'
            
    def save(self, commit=True):
        user = super().save(commit=False)
        # If it's an admin user, we can set user_role to admin. If it's a regular user, it stays 'customer'.
        if self.cleaned_data.get('user_role') == 'admin' and user.is_superuser:
            user.user_role = 'admin'
        else:
            user.user_role = 'customer'
        if commit:
            user.save()
        return user