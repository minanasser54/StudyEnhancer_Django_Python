from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2','email','first_name','last_name']
        help_texts={'email':'enter your Gmail'}

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        help_texts={'email':'enter your Gmail'}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['education_position','bio','grade','img']
