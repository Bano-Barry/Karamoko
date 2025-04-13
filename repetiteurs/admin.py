from django.contrib import admin
from .models import Repetiteur, Competence, Cours

# Enregistrement du modèle Competence
@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')  # Affiche l'ID et le nom dans la liste d'administration
    search_fields = ('nom',)  # Ajoute une barre de recherche sur le champ "nom"
    ordering = ('nom',)  # Trie les résultats par nom

# Enregistrement du modèle Repetiteur
@admin.register(Repetiteur)
class RepetiteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'email', 'contact')  # Affiche l'ID, le nom, l'email et le contact
    search_fields = ('nom', 'email', 'contact')  # Barre de recherche sur le nom, l'email et le contact
    list_filter = ('competences',)  # Ajoute un filtre par compétences
    ordering = ('nom',)  # Trie les résultats par nom
    filter_horizontal = ('competences',)  # Ajoute une interface pour gérer les relations ManyToMany

# Enregistrement du modèle Cours
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'niveau', 'repetiteur')  # Affiche l'ID, le titre, le niveau et le répétiteur
    search_fields = ('titre', 'niveau__nom', 'repetiteur__nom')  # Barre de recherche sur le titre, le niveau et le répétiteur
    list_filter = ('niveau', 'repetiteur')  # Ajoute des filtres par niveau et répétiteur
    ordering = ('titre',)  # Trie les résultats par titre
