from django import forms
from django.contrib.auth.models import User
from .models import *


class UserRegisterForm(forms.Form):
    error_message = {
        'min_length': 'please insert more than 5 character',
        'required': 'field is required',
        'invalid': 'email na motabar',
    }
    user_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Insert username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Insert mail'}), error_messages=error_message)
    first_name = forms.CharField(max_length=200, min_length=5, error_messages=error_message,
                                 widget=forms.TextInput(attrs={'placeholder': 'Insert first name'}))
    last_name = forms.CharField(max_length=200)
    password_1 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Insert Pass'}))
    password_2 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Pass'}))

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('User exists')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email exists')
        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']

        if password_1 != password_2:
            raise forms.ValidationError('Password not match')
        elif len(password_2) < 8:
            raise forms.ValidationError('Password too short')
        # elif not any(x.issuper() for x in password_2):
        #     raise forms.ValidationError('Please use on or more capital character')

        return password_2


class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_image']


class PhoneForm(forms.Form):
    phone = forms.IntegerField()


class CodeForm(forms.Form):
    code = forms.IntegerField()
