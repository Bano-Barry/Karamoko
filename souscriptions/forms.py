from django import forms

from core.models import Niveau
from paiements.models import OffreTarifaire
from repetiteurs.models import Cours
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
        fields = ['nombre_enfants', 'niveau', 'matieres', 'offre_tarifaire', 'creneaux_preferes', 'moyen_paiement', 'commentaire']
        labels = {
            'niveau': "Niveau Scolaire",
            'matieres': "Matières",
            'nombre_enfants': "Nombre d'enfants",
            'offre_tarifaire': "Offre Tarifaire",
            'creneaux_preferes': "Créneaux préférés",
            'moyen_paiement': "Moyen de Paiement",
            'commentaire': "Besoins spécifiques (facultatif)",
        }
        widgets = {
            'niveau': forms.Select(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'id': 'id_niveau'
            }),
            'matieres': forms.CheckboxSelectMultiple(attrs={
                'class': 'matiere-checkbox'
            }),
            'nombre_enfants': forms.NumberInput(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'min': '1',
                'max': '10'
            }),
            'offre_tarifaire': forms.RadioSelect(attrs={
                'class': 'offre-radio'
            }),
            'creneaux_preferes': forms.CheckboxSelectMultiple(attrs={
                'class': 'creneau-checkbox'
            }),
            'moyen_paiement': forms.Select(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Décrivez vos besoins spécifiques...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialiser les créneaux
        self.fields['creneaux_preferes'] = forms.MultipleChoiceField(
            choices=DemandeSouscription.CRENEAU_CHOICES,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'creneau-checkbox'}),
            required=False
        )
        
        # Si on a un niveau sélectionné, filtrer les matières et offres
        if 'niveau' in self.data:
            try:
                niveau_id = int(self.data.get('niveau'))
                niveau = Niveau.objects.get(id=niveau_id)
                
                # Filtrer les matières selon le niveau
                self.fields['matieres'].queryset = niveau.cours.all()
                
                # Filtrer les offres tarifaires selon le niveau
                self.fields['offre_tarifaire'].queryset = OffreTarifaire.objects.filter(
                    niveaux=niveau, is_active=True
                )
                
            except (ValueError, TypeError, Niveau.DoesNotExist):
                self.fields['matieres'].queryset = Cours.objects.none()
                self.fields['offre_tarifaire'].queryset = OffreTarifaire.objects.none()
        else:
            # Par défaut, pas de matières ni d'offres visibles
            self.fields['matieres'].queryset = Cours.objects.none()
            self.fields['offre_tarifaire'].queryset = OffreTarifaire.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        niveau = cleaned_data.get('niveau')
        matieres = cleaned_data.get('matieres')
        offre_tarifaire = cleaned_data.get('offre_tarifaire')
        
        # Vérifier que les matières correspondent au niveau
        if niveau and matieres:
            matieres_niveau = set(niveau.cours.all())
            matieres_selectionnees = set(matieres)
            
            if not matieres_selectionnees.issubset(matieres_niveau):
                raise forms.ValidationError(
                    "Certaines matières sélectionnées ne correspondent pas au niveau choisi."
                )
        
        # Vérifier que l'offre correspond au niveau
        if niveau and offre_tarifaire:
            if not offre_tarifaire.est_compatible_avec_niveau(niveau):
                raise forms.ValidationError(
                    "L'offre tarifaire sélectionnée n'est pas compatible avec le niveau choisi."
                )
        
        return cleaned_data