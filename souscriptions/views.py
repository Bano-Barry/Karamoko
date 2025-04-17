from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Souscription
from .forms import SouscriptionForm

# Liste des souscriptions
class SouscriptionListView(ListView):
    model = Souscription
    template_name = 'souscriptions/souscription_list.html'
    context_object_name = 'souscriptions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscriptions', 'url': None},
        ]
        return context

# Création d'une souscription
class SouscriptionCreateView(CreateView):
    model = Souscription
    template_name = 'souscriptions/souscription_form.html'
    form_class = SouscriptionForm
    success_url = reverse_lazy('souscription_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscriptions', 'url': 'souscription_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

# Mise à jour d'une souscription
class SouscriptionUpdateView(UpdateView):
    model = Souscription
    template_name = 'souscriptions/souscription_form.html'
    form_class = SouscriptionForm
    success_url = reverse_lazy('souscription_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscriptions', 'url': 'souscription_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

# Suppression d'une souscription
class SouscriptionDeleteView(DeleteView):
    model = Souscription
    template_name = 'souscriptions/souscription_confirm_delete.html'
    success_url = reverse_lazy('souscription_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscriptions', 'url': 'souscription_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context

