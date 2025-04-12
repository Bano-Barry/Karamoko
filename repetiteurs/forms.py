from django import forms
from .models import Repetiteur

class RepetiteurForm(forms.ModelForm):
    class Meta:
        model = Repetiteur
        fields = '__all__'  # Inclut tous les champs du modèle dans le formulaire