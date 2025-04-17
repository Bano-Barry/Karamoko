from django import forms
from .models import TypeFormation

class TypeFormationForm(forms.ModelForm):
    class Meta:
        model = TypeFormation
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea border border-gray-300 rounded-lg'}),            # Add widgets for other fields as needed
        }