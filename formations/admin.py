from django.contrib import admin
from .models import Formation, TypeFormation

# Enregistrement du modèle TypeFormation
@admin.register(TypeFormation)
class TypeFormationAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')  # Affiche l'ID et le nom dans la liste d'administration
    search_fields = ('nom',)  # Ajoute une barre de recherche sur le champ "nom"
    ordering = ('nom',)  # Trie les résultats par nom

# Enregistrement du modèle Formation
@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'type_formation')  # Affiche l'ID, le titre et le type de formation
    search_fields = ('titre', 'type_formation__nom')  # Barre de recherche sur le titre et le type de formation
    list_filter = ('type_formation',)  # Ajoute un filtre par type de formation
    ordering = ('titre',)  # Trie les résultats par titre
