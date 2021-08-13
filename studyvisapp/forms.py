from django import forms
from .models import TimeModel


class HomeForm(forms.ModelForm):
    class Meta:
        model = TimeModel
        fields = ("item",)
