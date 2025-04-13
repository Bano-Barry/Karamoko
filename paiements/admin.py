from django.contrib import admin
from .models import Paiement, MethodePaiement, PlanTarifaire

# Enregistrement du modèle MethodePaiement
@admin.register(MethodePaiement)
class MethodePaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')  # Affiche l'ID et le nom dans la liste d'administration
    search_fields = ('nom',)  # Ajoute une barre de recherche sur le champ "nom"
    ordering = ('nom',)  # Trie les résultats par nom

# Enregistrement du modèle PlanTarifaire
@admin.register(PlanTarifaire)
class PlanTarifaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prix')  # Affiche l'ID, le nom et le prix dans la liste d'administration
    search_fields = ('nom',)  # Ajoute une barre de recherche sur le champ "nom"
    list_filter = ('prix',)  # Ajoute un filtre par prix
    ordering = ('nom',)  # Trie les résultats par nom

# Enregistrement du modèle Paiement
@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'souscription', 'methode', 'montant', 'date')  # Affiche les détails du paiement
    search_fields = ('souscription__id', 'methode__nom')  # Barre de recherche sur la souscription et la méthode de paiement
    list_filter = ('methode', 'date')  # Ajoute des filtres par méthode de paiement et date
    ordering = ('-date',)  # Trie les paiements par date décroissante
