from django import forms

from .models import Souscripteur  # Importation du modèle Souscripteur depuis le fichier models.py

# Définition d'un formulaire basé sur le modèle Souscripteur
class SouscripteurForm(forms.ModelForm):
    # Classe interne Meta pour configurer le formulaire
    class Meta:
        model = Souscripteur  # Spécifie le modèle associé au formulaire
        fields = '__all__'  # Inclut tous les champs du modèle dans le formulaire
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez le nom',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez le prénom',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez l\'email',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Entrez le contact',
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
        }  # Fin correcte du dictionnaire widgets
        
class SouscripteurProfileForm(forms.ModelForm):
    class Meta:
        model = Souscripteur
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white',
            }),
        }