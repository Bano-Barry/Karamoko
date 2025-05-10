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
    list_display = ('id', 'user', 'user_email', 'user_phone')  # Affiche l'ID, le nom, l'email et le contact
    search_fields = ('user__username', 'user__email', 'user__phone')  # Barre de recherche sur le nom, l'email et le contact
    list_filter = ('competences',)  # Ajoute un filtre par compétences
    ordering = ('user__username',)  # Trie les résultats par nom
    filter_horizontal = ('competences', 'cours')  # Ajoute une interface pour gérer les relations ManyToMany

    # Méthodes pour afficher les champs liés
    @admin.display(description="Email")
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description="Téléphone")
    def user_phone(self, obj):
        return obj.user.phone

# Enregistrement du modèle Cours
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'description')  # Affiche l'ID, le titre et la description
    search_fields = ('titre', 'description')  # Barre de recherche sur le titre et la description
    ordering = ('titre',)  # Trie les résultats par titre