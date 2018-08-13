from django import forms
from django.conf import settings


class DayResultForm(forms.Form):
    base_day = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)



