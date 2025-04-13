from django.shortcuts import render, get_object_or_404, redirect
from .models import Repetiteur
from .forms import RepetiteurForm

def repetiteur_list(request):
    context = {
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Répétiteurs', 'url': 'repetiteur_list'},
            {'name': 'Liste des Répétiteurs', 'url': None},  # Pas de lien pour l'élément actif
        ],
        'repetiteurs': Repetiteur.objects.all(),
    }
    return render(request, 'repetiteurs/list.html', context)

def repetiteur_create(request):
    if request.method == 'POST':
        form = RepetiteurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('repetiteur_list')
    else:
        form = RepetiteurForm()
    
    context = {
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Répétiteurs', 'url': 'repetiteur_list'},
            {'name': 'Créer un Répétiteur', 'url': None},  # Pas de lien pour l'élément actif
        ],
        'form': form,
    }
    return render(request, 'repetiteurs/create.html', context)

def repetiteur_detail(request, id):
    repetiteur = get_object_or_404(Repetiteur, id=id)
    context = {
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Répétiteurs', 'url': 'repetiteur_list'},
            {'name': 'Détails du Répétiteur', 'url': None},  # Pas de lien pour l'élément actif
        ],
        'repetiteur': repetiteur,
    }
    return render(request, 'repetiteurs/detail.html', context)

def repetiteur_update(request, pk):
    repetiteur = get_object_or_404(Repetiteur, pk=pk)
    if request.method == 'POST':
        form = RepetiteurForm(request.POST, request.FILES, instance=repetiteur)
        if form.is_valid():
            form.save()
            return redirect('repetiteur_list')
    else:
        form = RepetiteurForm(instance=repetiteur)
    
    context = {
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Répétiteurs', 'url': 'repetiteur_list'},
            {'name': 'Modifier un Répétiteur', 'url': None},  # Pas de lien pour l'élément actif
        ],
        'form': form,
    }
    return render(request, 'repetiteurs/update.html', context)

def repetiteur_delete(request, pk):
    repetiteur = get_object_or_404(Repetiteur, pk=pk)
    if request.method == 'POST':
        repetiteur.delete()
        return redirect('repetiteur_list')
    return render(request, 'repetiteurs/delete.html', {'repetiteur': repetiteur})