from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Event

class GeneratorForm(forms.Form):
    title = forms.CharField(max_length=254)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'begin', 'end', 'youtube', 'manager']
        widgets = {
            'begin': DateTimePickerInput(options={"showClose": False}).start_of('event'),
            'end': DateTimePickerInput(options={"showClose": False}).end_of('event'),
        }
