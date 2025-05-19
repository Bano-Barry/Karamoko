from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from paiements.models import PlanTarifaire
from souscripteurs.models import Souscripteur
from souscriptions.models import Souscription
from .models import Competence, Repetiteur, Cours
from .forms import CompetenceForm, RepetiteurCreateForm, CoursForm, RepetiteurUpdateForm
from django.contrib import messages

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def repetiteur_list(request):
    adresse = request.GET.get('adresse', '').strip()
    competence = request.GET.get('competence', '').strip()

    repetiteurs = Repetiteur.objects.all()

    if adresse:
        repetiteurs = repetiteurs.filter(user__adresse__icontains=adresse)

    if competence:
        repetiteurs = repetiteurs.filter(competences__nom__icontains=competence)

    # Évite les doublons si un répétiteur a plusieurs compétences
    repetiteurs = repetiteurs.distinct()

    context = {
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Répétiteurs', 'url': 'repetiteur_list'},
            {'name': 'Liste des Répétiteurs', 'url': None},
        ],
        'repetiteurs': repetiteurs,
        'adresse': adresse,
        'competence': competence,
    }

    return render(request, 'repetiteurs/list.html', context)

@user_passes_test(is_superuser)
def vitrine_repetiteur_list(request):
    # Récupérer les paramètres GET
    adresse = request.GET.get('adresse', '').strip()
    competence = request.GET.get('competences', '').strip()

    # Récupérer tous les répétiteurs
    repetiteurs = Repetiteur.objects.all()

    # Appliquer les filtres
    if adresse:
        repetiteurs = repetiteurs.filter(user__adresse__icontains=adresse)

    if competence:
        repetiteurs = repetiteurs.filter(competences__nom__icontains=competence)

    # Éviter les doublons si un répétiteur a plusieurs compétences
    repetiteurs = repetiteurs.distinct()

    # Contexte pour le template
    context = {
        'repetiteurs': repetiteurs,
        'adresse': adresse,
        'competences': competence,
    }

    return render(request, 'vitrine/encadreurs.html', context)

@user_passes_test(is_superuser)
def repetiteur_create(request):
    if request.method == 'POST':
        form = RepetiteurCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('repetiteur_list')
    else:
        form = RepetiteurCreateForm()
    
    context = {
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Répétiteurs', 'url': 'repetiteur_list'},
            {'name': 'Créer un Répétiteur', 'url': None},  # Pas de lien pour l'élément actif
        ],
        'form': form,
    }
    return render(request, 'repetiteurs/create.html', context)

@user_passes_test(is_superuser)
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

def repetiteur_public_detail(request, id):
    repetiteur = get_object_or_404(Repetiteur, id=id)
    return render(request, 'repetiteurs/public_detail.html', {'repetiteur': repetiteur})

@user_passes_test(is_superuser)
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

@user_passes_test(is_superuser)
def repetiteur_delete(request, pk):
    repetiteur = get_object_or_404(Repetiteur, pk=pk)
    if request.method == 'POST':
        repetiteur.delete()
        return redirect('repetiteur_list')
    return render(request, 'repetiteurs/delete.html', {'repetiteur': repetiteur})

@method_decorator(user_passes_test(is_superuser), name='dispatch')
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

@method_decorator(user_passes_test(is_superuser), name='dispatch')
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
@method_decorator(user_passes_test(is_superuser), name='dispatch')
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
@method_decorator(user_passes_test(is_superuser), name='dispatch')
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
@method_decorator(user_passes_test(is_superuser), name='dispatch')
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
@method_decorator(user_passes_test(is_superuser), name='dispatch')
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
@method_decorator(user_passes_test(is_superuser), name='dispatch')
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
@method_decorator(user_passes_test(is_superuser), name='dispatch')
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

@login_required
def souscription_create(request, repetiteur_id):
    repetiteur = get_object_or_404(Repetiteur, id=repetiteur_id)
    souscripteur = get_object_or_404(Souscripteur, user=request.user)
    plans = PlanTarifaire.objects.all()

    if request.method == 'POST':
        cours_ids = request.POST.getlist('cours')
        plan_tarifaire_id = request.POST.get('plan_tarifaire')
        try:
            plan_tarifaire = get_object_or_404(PlanTarifaire, id=plan_tarifaire_id)

            date_debut = now().date()
            date_fin = date_debut + timedelta(days=30 * plan_tarifaire.duree)

            souscription = Souscription.objects.create(
                souscripteur=souscripteur,
                repetiteur=repetiteur,
                plan_tarifaire=plan_tarifaire,
                date_debut=date_debut,
                date_fin=date_fin,
                statut='active'
            )

            for cours_id in cours_ids:
                cours = get_object_or_404(Cours, id=cours_id)
                souscription.cours.add(cours)
            # print(f"Souscription créée avec ID : {souscription.id}")
            messages.success(request, "Souscription créée avec succès.")
            return redirect('souscription_detail', souscription_id=souscription.id)
        except Exception as e:
            messages.error(request, "Erreur lors de la création de la souscription.")

    # Si GET, afficher le formulaire
    date_today = now().date()
    date_fin = date_today + timedelta(days=30)  # Date par défaut (ex. 1 mois)
    return render(request, 'repetiteurs/souscription.html', {
        'repetiteur': repetiteur,
        'plans': plans,
        'date_today': date_today,
        'date_fin': date_fin,
    })