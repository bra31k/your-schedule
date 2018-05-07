from django import forms

from .models import PersonalVotes

class PersonalVotesForm(forms.ModelForm):

    class Meta:
        model = PersonalVotes
        fields = ['userName','selected_day']