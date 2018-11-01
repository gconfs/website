from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class EventGenForm(forms.Form):
    title = forms.CharField(max_length=254)