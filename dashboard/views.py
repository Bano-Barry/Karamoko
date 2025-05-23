from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_home(request):
    user = request.user
    context = {}

    if user.role == 'repetiteur':
        context['dashboard_type'] = 'repetiteur'
        # tu peux précharger des stats, cours, etc.
    elif user.role == 'parent':
        context['dashboard_type'] = 'parent'
        # tu peux charger les souscriptions, enfants, etc.
    elif user.is_superuser:
        context['dashboard_type'] = 'admin'
        # même logique ici
    return render(request, 'dashboard/home.html', context)  # Page d'accueil avec la structure globale

# Create your views here.
