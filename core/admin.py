from django.contrib import admin
from .models import (
    TypeFormation, Competence, Niveau, Repetiteur, Cours,
    Souscripteur, PlanTarifaire, Souscription, MethodePaiement, Paiement
)

admin.site.register(TypeFormation)
admin.site.register(Competence)
admin.site.register(Niveau)
admin.site.register(Repetiteur)
admin.site.register(Cours)
admin.site.register(Souscripteur)
admin.site.register(PlanTarifaire)
admin.site.register(Souscription)
admin.site.register(MethodePaiement)
admin.site.register(Paiement)
