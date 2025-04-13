from django.contrib import admin
from .models import Souscripteur

# Enregistrement du modèle Souscripteur
@admin.register(Souscripteur)
class SouscripteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'prenom', 'email', 'contact')  # Affiche l'ID, le nom, l'email et le contact
    search_fields = ('nom', 'email', 'contact')  # Ajoute une barre de recherche sur le nom, l'email et le contact
    ordering = ('nom',)  # Trie les résultats par nom
