from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    # email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
