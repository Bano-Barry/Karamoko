from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from souscriptions.models import DemandeSouscription, Souscription

@login_required
def dashboard_home(request):
    user = request.user
    context = {}

    if user.role == 'repetiteur':
        context['dashboard_type'] = 'repetiteur'
        repetiteur = user.repetiteur
        souscriptions = Souscription.objects.filter(repetiteur=repetiteur)
        context['souscriptions'] = souscriptions
        # print("Souscriptions récupérées pour:", repetiteur)
        # print('User:', user)

        # souscriptions, stats, cours, etc.
    elif user.role == 'parent':
        context['dashboard_type'] = 'parent'
        demandes = DemandeSouscription.objects.filter(souscripteur__user=user)
        context['demandes'] = demandes
        # souscriptions, enfants, etc.
    elif user.is_superuser:
        context['dashboard_type'] = 'admin'
        # Statistiques globales, gestion des utilisateurs, etc.
    return render(request, 'dashboard/home.html', context)  # Page d'accueil avec la structure globale

# Create your views here.
