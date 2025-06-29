from django import forms
from .models import Client, Commission, Character

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nickname', 'handle', 'email', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        exclude = ['client']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        exclude = ['client']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }