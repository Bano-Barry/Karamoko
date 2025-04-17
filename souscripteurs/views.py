from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Souscripteur
from .forms import SouscripteurForm

# Liste des souscripteurs
class SouscripteurListView(ListView):
    model = Souscripteur
    template_name = 'souscripteurs/list.html'
    context_object_name = 'souscripteurs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscripteurs', 'url': 'souscripteur_list'},
            {'name': 'Liste des Souscripteurs', 'url': None},
        ]
        return context

# Détail d'un souscripteur
class SouscripteurDetailView(DetailView):
    model = Souscripteur
    template_name = 'souscripteurs/detail.html'
    context_object_name = 'souscripteur'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscripteurs', 'url': 'souscripteur_list'},
            {'name': 'Détail du Souscripteur', 'url': None},
        ]
        return context

# Création d'un souscripteur
class SouscripteurCreateView(CreateView):
    model = Souscripteur
    template_name = 'souscripteurs/create.html'
    form_class = SouscripteurForm
    success_url = reverse_lazy('souscripteur_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscripteurs', 'url': 'souscripteur_list'},
            {'name': 'Créer un Souscripteur', 'url': None},
        ]
        return context

# Mise à jour d'un souscripteur
class SouscripteurUpdateView(UpdateView):
    model = Souscripteur
    template_name = 'souscripteurs/create.html'
    form_class = SouscripteurForm
    success_url = reverse_lazy('souscripteur_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscripteurs', 'url': 'souscripteur_list'},
            {'name': 'Modifier un Souscripteur', 'url': None},
        ]
        return context

# Suppression d'un souscripteur
class SouscripteurDeleteView(DeleteView):
    model = Souscripteur
    template_name = 'souscripteurs/delete.html'
    success_url = reverse_lazy('souscripteur_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscripteurs', 'url': 'souscripteur_list'},
            {'name': 'Supprimer un Souscripteur', 'url': None},
        ]
        return context
