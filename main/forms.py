from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Wing, Fuselage, Tail , Avionics, Aircraft

class RegistrationForm(UserCreationForm):
    team_choices = (
        ('wing', 'Wing Team'),
        ('fuselage', 'Fuselage Team'),
        ('tail', 'Tail Team'),
        ('avionics', 'Avionics Team'),
        ('assembly', 'Assembly Team')
    )
    email = forms.EmailField(required=True)
    team = forms.ChoiceField(help_text="Select a Team", choices=team_choices)

    class Meta:
        model = User
        fields = ["username",  "email", "password1", "password2" , "team"]

class WingForm(forms.ModelForm):
    class Meta:
        model = Wing
        fields = ["wing_type"]

class FuselageForm(forms.ModelForm):
    class Meta:
        model = Fuselage
        fields = ["fuselage_type"]

class TailForm(forms.ModelForm):
    class Meta:
        model = Tail
        fields = ["tail_type"]

class AvionicsForm(forms.ModelForm):
    class Meta:
        model = Avionics
        fields = ["avionics_type"]

class AssemblyForm(forms.ModelForm):
    class Meta:
        model = Aircraft
        fields = ["aircraft_type"]