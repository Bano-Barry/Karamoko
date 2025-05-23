from django import forms
from .models import Niveau

class NiveauForm(forms.ModelForm):
    class Meta:
        model = Niveau
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'block w-full mt-1 px-4 py-3 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez le nom du niveau',
            }),
        }