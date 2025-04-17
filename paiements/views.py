from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import MethodePaiement, PlanTarifaire, Paiement

# Vues pour MethodePaiement
class MethodePaiementListView(ListView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_list.html'
    context_object_name = 'methodes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse_lazy('dashboard_home')},
            {'name': 'Méthodes de Paiement', 'url': None},
        ]
        return context

class MethodePaiementCreateView(CreateView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_form.html'
    fields = ['nom']
    success_url = reverse_lazy('methodepaiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Accueil', 'url': reverse_lazy('dashboard_home')},
            {'name': 'Méthodes de Paiement', 'url': reverse_lazy('methodepaiement_list')},
            {'name': 'Créer', 'url': None},
        ]
        return context

class MethodePaiementUpdateView(UpdateView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_form.html'
    fields = ['nom']
    success_url = reverse_lazy('methodepaiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Accueil', 'url': reverse_lazy('dashboard_home')},
            {'name': 'Méthodes de Paiement', 'url': reverse_lazy('methodepaiement_list')},
            {'name': 'Modifier', 'url': None},
        ]
        return context

class MethodePaiementDeleteView(DeleteView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_confirm_delete.html'
    success_url = reverse_lazy('methodepaiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Accueil', 'url': reverse_lazy('dashboard_home')},
            {'name': 'Méthodes de Paiement', 'url': reverse_lazy('methodepaiement_list')},
            {'name': 'Supprimer', 'url': None},
        ]
        return context

# Vous pouvez appliquer la même logique pour les vues PlanTarifaire et Paiement.
