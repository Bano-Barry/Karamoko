from django.contrib import admin
from .models import Souscripteur

# Enregistrement du modèle Souscripteur
@admin.register(Souscripteur)
class SouscripteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__first_name', 'user__email', 'user__phone')  # Affiche l'ID, le nom, l'email et le contact
    search_fields = ('user__last_name', 'user__email', 'user__phone')  # Ajoute une barre de recherche sur le nom, l'email et le contact
    ordering = ('user__last_name',)  # Trie les résultats par nom
