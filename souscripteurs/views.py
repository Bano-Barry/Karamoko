from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Souscripteur
from .forms import SouscripteurForm

# Create your views here.
def index(request):
    souscripteurs = Souscripteur.objects.all()
    return render(request, 'souscripteurs/list.html', {'souscripteurs': souscripteurs})

def create_souscripteur(request):
    if request.method == 'POST':
        form = SouscripteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SouscripteurForm()
    return render(request, 'souscripteurs/create.html', {'form': form})

def detail_souscripteur(request, id):
    souscripteur = get_object_or_404(Souscripteur, id=id)
    return render(request, 'souscripteurs/detail.html', {'souscripteur': souscripteur})

def update_souscripteur(request, id):
    souscripteur = get_object_or_404(Souscripteur, id=id)
    if request.method == 'POST':
        form = SouscripteurForm(request.POST, instance=souscripteur)
        if form.is_valid():
            form.save()
            return redirect('detail_souscripteur', id=id)
    else:
        form = SouscripteurForm(instance=souscripteur)
    return render(request, 'souscripteurs/update.html', {'form': form, 'souscripteur': souscripteur})

def delete_souscripteur(request, id):
    souscripteur = get_object_or_404(Souscripteur, id=id)
    if request.method == 'POST':
        souscripteur.delete()
        return redirect('index')
    return render(request, 'souscripteurs/delete.html', {'souscripteur': souscripteur})