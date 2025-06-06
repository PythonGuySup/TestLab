from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data
