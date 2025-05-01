from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Competence, Repetiteur, Cours
from .forms import CompetenceForm, RepetiteurForm, CoursForm, RepetiteurUpdateForm

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
    user_instance = repetiteur.user  # Récupérer l'utilisateur lié

    if request.method == 'POST':
        form = RepetiteurUpdateForm(request.POST, request.FILES, instance=repetiteur, user_instance=user_instance)
        if form.is_valid():
            form.save()
            return redirect('repetiteur_list')
    else:
        form = RepetiteurUpdateForm(instance=repetiteur, user_instance=user_instance)
    
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

# Liste des compétences
class CompetenceListView(ListView):
    model = Competence
    template_name = 'repetiteurs/competence_list.html'
    context_object_name = 'competences'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Compétences', 'url': None},
        ]
        return context

# Création d'une compétence
class CompetenceCreateView(CreateView):
    model = Competence
    template_name = 'repetiteurs/competence_form.html'
    form_class = CompetenceForm
    success_url = reverse_lazy('competence_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Compétences', 'url': 'competence_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

# Mise à jour d'une compétence
class CompetenceUpdateView(UpdateView):
    model = Competence
    template_name = 'repetiteurs/competence_form.html'
    form_class = CompetenceForm
    success_url = reverse_lazy('competence_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Compétences', 'url': 'competence_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

# Suppression d'une compétence
class CompetenceDeleteView(DeleteView):
    model = Competence
    template_name = 'repetiteurs/competence_confirm_delete.html'
    success_url = reverse_lazy('competence_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Compétences', 'url': 'competence_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context

# Liste des cours
class CoursListView(ListView):
    model = Cours
    template_name = 'repetiteurs/cours_list.html'
    context_object_name = 'cours'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Cours', 'url': None},
        ]
        return context

# Création d'un cours
class CoursCreateView(CreateView):
    model = Cours
    template_name = 'repetiteurs/cours_form.html'
    form_class = CoursForm
    success_url = reverse_lazy('cours_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Cours', 'url': 'cours_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

# Mise à jour d'un cours
class CoursUpdateView(UpdateView):
    model = Cours
    template_name = 'repetiteurs/cours_form.html'
    form_class = CoursForm
    success_url = reverse_lazy('cours_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Cours', 'url': 'cours_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

# Suppression d'un cours
class CoursDeleteView(DeleteView):
    model = Cours
    template_name = 'repetiteurs/cours_confirm_delete.html'
    success_url = reverse_lazy('cours_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Cours', 'url': 'cours_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context

