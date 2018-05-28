from django import forms
import datetime
from django.conf import settings
from .models import Company

class DayResultForm(forms.Form):
    base_day = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

