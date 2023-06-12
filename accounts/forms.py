from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

class ProfileSettingForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'image', 'self_introduction_text')