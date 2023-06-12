from django import forms
from .models import PartyPost, Awakening, Folder
from PIL import Image

class PartyPostForm(forms.ModelForm):
    class Meta:
        model = PartyPost
        fields = ['title', 'thumbnail', 'text']

class AwakeningForm(forms.ModelForm):
    class Meta:
        model = Awakening
        fields = ['skillboost', 'sealed_resistance', 'poison_resistance', 'obstacle_resistance', 'darkness_resistance', 'operation_resistance', 'cloud_resistance', 'operation_time']

