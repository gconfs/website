from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class GeneratorForm(forms.Form):
    title = forms.CharField(max_length=254)