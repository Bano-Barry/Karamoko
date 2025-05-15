from django import forms
from .models import MethodePaiement, PlanTarifaire, Paiement

# Utilitaire pour les widgets communs
def get_widget(input_type, placeholder, additional_classes=""):
    base_classes = (
        "block w-full mt-1 border-gray-300 px-4 py-3 rounded-md shadow-sm "
        "focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-800 "
        "dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
    )
    return input_type(attrs={
        'class': f"{base_classes} {additional_classes}",
        'placeholder': placeholder,
    })

class MethodePaiementForm(forms.ModelForm):
    class Meta:
        model = MethodePaiement
        fields = '__all__'
        widgets = {
            'nom': get_widget(forms.TextInput, 'Entrez le nom de la méthode de paiement'),
            'description': get_widget(forms.Textarea, 'Entrez la description de la méthode de paiement'),
        }

class PlanTarifaireForm(forms.ModelForm):
    class Meta:
        model = PlanTarifaire
        fields = '__all__'
        widgets = {
            'nom': get_widget(forms.TextInput, 'Entrez le nom du plan tarifaire'),
            'description': get_widget(forms.Textarea, 'Entrez la description du plan tarifaire'),
            'duree': get_widget(forms.NumberInput, 'Entrez la durée en jours'),
            'prix': get_widget(forms.NumberInput, 'Entrez le prix'),
        }

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'
        widgets = {
            'souscription': get_widget(forms.Select, '', additional_classes=''),
            'methode': get_widget(forms.Select, '', additional_classes=''),
            'montant': get_widget(forms.NumberInput, 'Entrez le montant'),
            'date': get_widget(forms.DateTimeInput, 'Entrez la date', additional_classes='datetime-local'),
            'statut': get_widget(forms.Select, '', additional_classes=''),
        }
