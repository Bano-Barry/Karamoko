from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.forms import NiveauForm
from .models import Niveau
from repetiteurs.models import Repetiteur

def home(request):
    return render(request, 'vitrine/home.html')

def encadreurs(request):
    repetiteurs = Repetiteur.objects.all()
    return render(request, 'vitrine/encadreurs.html', {'repetiteurs': repetiteurs})

def services(request):
    return render(request, 'vitrine/services.html')

def about(request):
    return render(request, 'vitrine/about.html')


# Liste des niveaux
class NiveauListView(ListView):
    model = Niveau
    template_name = 'core/niveau_list.html'
    context_object_name = 'niveaux'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': None},
        ]
        return context

# Création d'un niveau
class NiveauCreateView(CreateView):
    model = Niveau
    template_name = 'core/niveau_form.html'
    form_class = NiveauForm
    success_url = reverse_lazy('niveau_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': 'niveau_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

# Mise à jour d'un niveau
class NiveauUpdateView(UpdateView):
    model = Niveau
    template_name = 'core/niveau_form.html'
    form_class = NiveauForm
    success_url = reverse_lazy('niveau_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': 'niveau_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

# Suppression d'un niveau
class NiveauDeleteView(DeleteView):
    model = Niveau
    template_name = 'core/niveau_confirm_delete.html'
    success_url = reverse_lazy('niveau_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': 'niveau_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context
