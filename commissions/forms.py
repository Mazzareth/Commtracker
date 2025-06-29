from django import forms
from .models import Client, Commission, Character, ClientNote, CommissionNote

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
        exclude = ['client', 'reference_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class ClientNoteForm(forms.ModelForm):
    class Meta:
        model = ClientNote
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a note...'}),
        }

class CommissionNoteForm(forms.ModelForm):
    class Meta:
        model = CommissionNote
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a note...'}),
        }