from django.shortcuts import render, get_object_or_404, redirect
from .models import Repetiteur
from .forms import RepetiteurForm

def repetiteur_list(request):
    repetiteurs = Repetiteur.objects.all()
    return render(request, 'repetiteurs/list.html', {'repetiteurs': repetiteurs})

def repetiteur_create(request):
    if request.method == 'POST':
        form = RepetiteurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('repetiteur_list')
    else:
        form = RepetiteurForm()
    return render(request, 'repetiteurs/create.html', {'form': form})

def detail_repetiteur(request, id):
    repetiteur = get_object_or_404(Repetiteur, id=id)
    return render(request, 'repetiteurs/detail.html', {'repetiteur': repetiteur})

def repetiteur_update(request, pk):
    repetiteur = get_object_or_404(Repetiteur, pk=pk)
    if request.method == 'POST':
        form = RepetiteurForm(request.POST, request.FILES, instance=repetiteur)
        if form.is_valid():
            form.save()
            return redirect('repetiteur_list')
    else:
        form = RepetiteurForm(instance=repetiteur)
    return render(request, 'repetiteurs/update.html', {'form': form})

def repetiteur_delete(request, pk):
    repetiteur = get_object_or_404(Repetiteur, pk=pk)
    if request.method == 'POST':
        repetiteur.delete()
        return redirect('repetiteur_list')
    return render(request, 'repetiteurs/delete.html', {'repetiteur': repetiteur})