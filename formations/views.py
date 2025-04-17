from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from formations.forms import FormationForm, TypeFormationForm
from .models import TypeFormation, Formation

# Vues pour TypeFormation
class TypeFormationListView(ListView):
    model = TypeFormation
    template_name = 'formations/typeformation_list.html'
    context_object_name = 'typeformations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Types de Formation', 'url': None},
        ]
        return context

class TypeFormationCreateView(CreateView):
    model = TypeFormation
    template_name = 'formations/typeformation_form.html'
    # fields = ['nom']
    form_class = TypeFormationForm
    success_url = reverse_lazy('typeformation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Types de Formation', 'url': 'typeformation_list'},
            {'name': 'Créer un Type de Formation', 'url': None},
        ]
        return context

class TypeFormationUpdateView(UpdateView):
    model = TypeFormation
    template_name = 'formations/typeformation_form.html'
    # fields = ['nom', 'description']
    form_class = TypeFormationForm
    success_url = reverse_lazy('typeformation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Types de Formation', 'url': 'typeformation_list'},
            {'name': 'Modifier un Type de Formation', 'url': None},
        ]
        return context

class TypeFormationDeleteView(DeleteView):
    model = TypeFormation
    template_name = 'formations/typeformation_confirm_delete.html'
    success_url = reverse_lazy('typeformation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Types de Formation', 'url': 'typeformation_list'},
            {'name': 'Supprimer un Type de Formation', 'url': None},
        ]
        return context

# Vues pour Formation
class FormationListView(ListView):
    model = Formation
    template_name = 'formations/formation_list.html'
    context_object_name = 'formations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Formations', 'url': None},
        ]
        return context

class FormationCreateView(CreateView):
    model = Formation
    template_name = 'formations/formation_form.html'
    form_class = FormationForm
    success_url = reverse_lazy('formation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Formations', 'url': 'formation_list'},
            {'name': 'Créer une Formation', 'url': None},
        ]
        return context

class FormationUpdateView(UpdateView):
    model = Formation
    template_name = 'formations/formation_form.html'
    form_class = FormationForm
    success_url = reverse_lazy('formation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Formations', 'url': 'formation_list'},
            {'name': 'Modifier une Formation', 'url': None},
        ]
        return context

class FormationDeleteView(DeleteView):
    model = Formation
    template_name = 'formations/formation_confirm_delete.html'
    success_url = reverse_lazy('formation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Formations', 'url': 'formation_list'},
            {'name': 'Supprimer une Formation', 'url': None},
        ]
        return context
