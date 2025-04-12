from django import forms  # Importation du module forms de Django pour créer des formulaires
from .models import Souscripteur  # Importation du modèle Souscripteur depuis le fichier models.py

# Définition d'un formulaire basé sur le modèle Souscripteur
class SouscripteurForm(forms.ModelForm):
    # Classe interne Meta pour configurer le formulaire
    class Meta:
        model = Souscripteur  # Spécifie le modèle associé au formulaire
        fields = '__all__'  # Inclut tous les champs du modèle dans le formulaire