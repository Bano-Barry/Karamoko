from django.contrib import admin

from paiements.models import MethodePaiement, Paiement, PlanTarifaire

@admin.register(MethodePaiement)
class MethodePaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)
    ordering = ('nom',)

@admin.register(PlanTarifaire)
class PlanTarifaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prix', 'description_courte')
    search_fields = ('nom', 'description')
    list_filter = ('prix',)
    ordering = ('nom',)

    def description_courte(self, obj):
        return (obj.description[:50] + '...') if obj.description else "-"
    description_courte.short_description = 'Description'

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'get_souscripteur', 
        'get_repetiteur',
        # 'plan_tarifaire', 
        'methode', 
        'montant', 
        'date'
    )
    search_fields = (
        'souscription__souscripteur__nom', 
        'souscription__repetiteur__nom',
        'methode__nom'
    )
    list_filter = (
        'methode', 
        'date',
        # 'souscription__plan_tarifaire'
    )
    ordering = ('-date',)

    def get_souscripteur(self, obj):
        return obj.souscription.souscripteur.nom
    get_souscripteur.short_description = 'Souscripteur'

    def get_repetiteur(self, obj):
        return obj.souscription.repetiteur.nom
    get_repetiteur.short_description = 'Répetiteur'

    # def plan_tarifaire(self, obj):
    #     return obj.souscription.plan_tarifaire.nom
    # plan_tarifaire.short_description = 'Plan Tarifaire'
