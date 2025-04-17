from django import forms
from .models import Souscription

class SouscriptionForm(forms.ModelForm):
    class Meta:
        model = Souscription
        fields = '__all__'
        widgets = {
            'souscripteur': forms.Select(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'repetiteur': forms.Select(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'plan_tarifaire': forms.Select(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
            'date_debut': forms.DateInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'type': 'date',
            }),
            'date_fin': forms.DateInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'type': 'date',
            }),
        }