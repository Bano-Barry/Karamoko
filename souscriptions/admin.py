from django.contrib import admin

from souscriptions.models import Evaluation, PasserSeance, Souscription

# Inline pour afficher les séances dans la fiche d'une souscription
class PasserSeanceInline(admin.TabularInline):
    model = PasserSeance
    extra = 1  # Nombre de lignes vides par défaut

# Inline pour afficher l'évaluation
class EvaluationInline(admin.StackedInline):
    model = Evaluation
    can_delete = False
    extra = 0

@admin.register(Souscription)
class SouscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'souscripteur', 
        'repetiteur', 
        'plan_tarifaire', 
        'get_cours',
        'statut', 
        'date_debut', 
        'date_fin'
    )
    search_fields = (
        'souscripteur__nom', 
        'repetiteur__nom', 
        'plan_tarifaire__nom',
        'cours__nom'
    )
    list_filter = (
        'statut',
        'plan_tarifaire', 
        'cours',
        'date_debut', 
        'date_fin'
    )
    ordering = ('-date_debut',)
    inlines = [PasserSeanceInline, EvaluationInline]

    def get_cours(self, obj):
        return ", ".join([c.nom for c in obj.cours.all()])
    get_cours.short_description = 'Cours'

@admin.register(PasserSeance)
class PasserSeanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'souscription', 'date', 'commentaire')
    search_fields = (
        'souscription__souscripteur__nom', 
        'souscription__repetiteur__nom'
    )
    list_filter = ('date',)
    ordering = ('-date',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('souscription', 'note', 'commentaire')
    search_fields = (
        'souscription__souscripteur__nom',
        'souscription__repetiteur__nom',
        'commentaire'
    )
    list_filter = ('note',)
    ordering = ('-note',)
