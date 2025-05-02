from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Souscripteur
from .forms import SouscripteurCreateForm, SouscripteurUpdateForm


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
    form_class = SouscripteurCreateForm
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
    form_class = SouscripteurUpdateForm
    success_url = reverse_lazy('souscripteur_list')

    def get_object(self, queryset=None):
        # Récupérer l'instance du souscripteur
        souscripteur = super().get_object(queryset)
        self.user_instance = souscripteur.user  # Récupérer l'utilisateur lié
        return souscripteur

    def get_form_kwargs(self):
        # Ajouter l'utilisateur lié aux kwargs du formulaire
        kwargs = super().get_form_kwargs()
        kwargs['user_instance'] = self.user_instance
        return kwargs

    def form_valid(self, form):
        # Sauvegarder les données du formulaire
        souscripteur = form.save(commit=False)

        # Mettre à jour les champs de l'utilisateur lié
        if self.user_instance:
            self.user_instance.email = form.cleaned_data.get('email', self.user_instance.email)
            self.user_instance.username = form.cleaned_data.get('username', self.user_instance.username)
            self.user_instance.first_name = form.cleaned_data.get('first_name', self.user_instance.first_name)
            self.user_instance.last_name = form.cleaned_data.get('last_name', self.user_instance.last_name)
            self.user_instance.save()

        souscripteur.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Ajouter des informations supplémentaires au contexte
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
