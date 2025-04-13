from django.contrib import admin
from .models import Souscription, PasserSeance

# Enregistrement du modèle Souscription
@admin.register(Souscription)
class SouscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'souscripteur', 'repetiteur', 'plan_tarifaire', 'date_debut', 'date_fin')  # Affiche les détails de la souscription
    search_fields = ('souscripteur__nom', 'repetiteur__nom', 'plan_tarifaire__nom')  # Barre de recherche sur le souscripteur, le répétiteur et le plan tarifaire
    list_filter = ('plan_tarifaire', 'date_debut', 'date_fin')  # Ajoute des filtres par plan tarifaire et dates
    ordering = ('-date_debut',)  # Trie les souscriptions par date de début décroissante

# Enregistrement du modèle PasserSeance
@admin.register(PasserSeance)
class PasserSeanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'souscription', 'date', 'commentaire')  # Affiche les détails de la séance
    search_fields = ('souscription__souscripteur__nom', 'souscription__repetiteur__nom')  # Barre de recherche sur le souscripteur et le répétiteur
    list_filter = ('date',)  # Ajoute un filtre par date
    ordering = ('-date',)  # Trie les séances par date décroissante
