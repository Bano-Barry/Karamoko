from django import forms
from .models import MethodePaiement, OffreTarifaire, PlanTarifaire, Paiement

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

class OffreTarifaireForm(forms.ModelForm):
    class Meta:
        model = OffreTarifaire
        fields = '__all__'
        labels = {
            'nom': 'Nom de l\'offre tarifaire',
            'description': 'Description de l\'offre tarifaire',
            'prix_unitaire': 'Prix unitaire (en GNF)',
            'prix_combine': 'Prix combiné (optionnel, en GNF)',
            'nombre_seances_mois': 'Nombre de séances par mois',
            'duree_seance_max': 'Durée maximale d\'une séance (en minutes)',
            'jours_par_semaine': 'Nombre de jours par semaine',
            'type_offre': 'Type d\'offre',
            'niveaux': 'Niveaux concernés',
        }
        widgets = {
            'nom': get_widget(forms.TextInput, 'Entrez le nom de l\'offre tarifaire'),
            'description': get_widget(forms.Textarea, 'Entrez la description de l\'offre tarifaire'),
            'prix_unitaire': get_widget(forms.NumberInput, 'Entrez le prix unitaire'),
            'prix_combine': get_widget(forms.NumberInput, 'Entrez le prix combiné (optionnel)'),
            'nombre_seances_mois': get_widget(forms.NumberInput, 'Entrez le nombre de séances par mois'),
            'duree_seance_max': get_widget(forms.NumberInput, 'Entrez la durée maximale d\'une séance en minutes'),
            'jours_par_semaine': get_widget(forms.NumberInput, 'Entrez le nombre de jours par semaine'),
            'type_offre': get_widget(forms.Select, '', additional_classes='select-type-offre'),
            'niveaux': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'matieres_incluses': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
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
