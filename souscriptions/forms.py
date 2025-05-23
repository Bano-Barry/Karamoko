from django import forms
from .models import DemandeSouscription, Souscription

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

class SouscriptionForm(forms.ModelForm):
    class Meta:
        model = Souscription
        fields = '__all__'
        widgets = {
            'souscripteur': get_widget(forms.Select, "Sélectionnez un souscripteur"),
            'repetiteur': get_widget(forms.Select, "Sélectionnez un répétiteur"),
            'cours': get_widget(forms.SelectMultiple, "Sélectionnez des cours"),
            'plan_tarifaire': get_widget(forms.Select, "Sélectionnez un plan tarifaire"),
            'date_debut': get_widget(forms.DateInput, "Sélectionnez une date de début", additional_classes="px-2", ),
            'date_fin': get_widget(forms.DateInput, "Sélectionnez une date de fin", additional_classes="px-2", ),
            'statut': get_widget(forms.Select, "Sélectionnez un statut"),
        }

class DemandeSouscriptionForm(forms.ModelForm):
    class Meta:
        model = DemandeSouscription
        fields = ['nombre_enfants', 'niveau', 'matieres',  'moyen_paiement', 'commentaire']
        widgets = {
            'niveau': get_widget(forms.Select, "Niveau Scolaire"),
            'matieres': forms.CheckboxSelectMultiple(),
            'nombre_enfants': get_widget(forms.NumberInput, "Nombre d'enfants", additional_classes="px-2"),
            'moyen_paiement': get_widget(forms.Select, "Sélectionnez un moyen de paiement"),
            'commentaire': get_widget(forms.Textarea, "Commentaire", additional_classes="px-2"),
        }