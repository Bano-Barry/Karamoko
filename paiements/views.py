from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import MethodePaiement, OffreTarifaire, Paiement
from .forms import MethodePaiementForm, OffreTarifaireForm, PaiementForm

# Vues pour MethodePaiement
class MethodePaiementListView(ListView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_list.html'
    context_object_name = 'methodes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Méthodes de Paiement', 'url': None},
        ]
        return context

class MethodePaiementCreateView(CreateView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_form.html'
    form_class = MethodePaiementForm
    success_url = reverse_lazy('methodepaiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Méthodes de Paiement', 'url': 'methodepaiement_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

class MethodePaiementUpdateView(UpdateView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_form.html'
    form_class = MethodePaiementForm
    success_url = reverse_lazy('methodepaiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Méthodes de Paiement', 'url': 'methodepaiement_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

class MethodePaiementDeleteView(DeleteView):
    model = MethodePaiement
    template_name = 'paiements/methodepaiement_confirm_delete.html'
    success_url = reverse_lazy('methodepaiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Méthodes de Paiement', 'url': 'methodepaiement_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context

# Vues pour PlanTarifaire
class PlanTarifaireListView(ListView):
    model = OffreTarifaire
    template_name = 'paiements/plantarifaire_list.html'
    context_object_name = 'plans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Plans Tarifaires', 'url': None},
        ]
        return context

class PlanTarifaireDetailView(DetailView):
    model = OffreTarifaire
    template_name = 'paiements/plantarifaire_detail.html'
    context_object_name = 'offertarifaire'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Plans Tarifaires', 'url': 'plantarifaire_list'},
            {'name': 'Détails', 'url': None},
        ]
        return context
    
class PlanTarifaireCreateView(CreateView):
    model = OffreTarifaire
    template_name = 'paiements/plantarifaire_form.html'
    form_class = OffreTarifaireForm
    success_url = reverse_lazy('plantarifaire_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Plans Tarifaires', 'url': 'plantarifaire_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

class PlanTarifaireUpdateView(UpdateView):
    model = OffreTarifaire
    template_name = 'paiements/plantarifaire_form.html'
    form_class = OffreTarifaireForm
    success_url = reverse_lazy('plantarifaire_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Plans Tarifaires', 'url': 'plantarifaire_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

class PlanTarifaireDeleteView(DeleteView):
    model = OffreTarifaire
    template_name = 'paiements/plantarifaire_confirm_delete.html'
    success_url = reverse_lazy('plantarifaire_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Plans Tarifaires', 'url': 'plantarifaire_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context

# Vues pour Paiement
class PaiementListView(ListView):
    model = Paiement
    template_name = 'paiements/paiement_list.html'
    context_object_name = 'paiements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Paiements', 'url': None},
        ]
        return context

class PaiementCreateView(CreateView):
    model = Paiement
    template_name = 'paiements/paiement_form.html'
    form_class = PaiementForm
    success_url = reverse_lazy('paiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Paiements', 'url': 'paiement_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

class PaiementUpdateView(UpdateView):
    model = Paiement
    template_name = 'paiements/paiement_form.html'
    form_class = PaiementForm
    success_url = reverse_lazy('paiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Paiements', 'url': 'paiement_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

class PaiementDeleteView(DeleteView):
    model = Paiement
    template_name = 'paiements/paiement_confirm_delete.html'
    success_url = reverse_lazy('paiement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Paiements', 'url': 'paiement_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context