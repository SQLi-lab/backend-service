from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Lab

from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'study_group']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают!')

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован!")
        return email


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

