from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

from .models import Customer


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ':'True', 'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']


class PasswordResetForm():
    pass

class CustomerprofileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city','state', 'mobile', 'zipcode']
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            "locality":forms.TextInput(attrs={'class': 'form-control'}),
            'city':forms.TextInput(attrs={'class': 'form-control'}),
            'mobile':forms.NumberInput(attrs={'class': 'form-control'}),
            'state':forms.Select(attrs={'class': 'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class': 'form-control'}),

        }