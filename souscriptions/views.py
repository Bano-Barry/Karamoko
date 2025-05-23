from datetime import timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from repetiteurs.models import Repetiteur
from .models import DemandeSouscription, Souscription
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

def affecter_demande_souscription(request, demande_id):
    demande = get_object_or_404(DemandeSouscription, id=demande_id, statut='en_attente')
    repetiteurs = Repetiteur.objects.filter(user__is_validated = True)
    if request.method == 'POST':
        repetiteur_id = request.POST.get('repetiteur')
        repetiteur = get_object_or_404(Repetiteur, id=repetiteur_id)
        souscription = Souscription.objects.create(
            souscripteur=demande.souscripteur,
            repetiteur=repetiteur,
            moyen_paiement=demande.moyen_paiement,
            date_debut=demande.date_demande,
            date_fin=demande.date_demande + timedelta(days=30),  # Exemple de durée de 30 jours
            statut='active'
        )
        souscription.cours.set(demande.matieres.all())
        demande.statut = 'affectée'
        demande.save()
        messages.success(request, "Demande de souscription affectée et créée avec succès.")
        return redirect('liste_demandes_souscription')

    return render(request, 'souscriptions/affecter_demande_souscription.html', {
            'demande': demande,
            # 'souscription': souscription,
            'repetiteurs': repetiteurs,
            'breadcrumb': [
                {'name': 'Dashboard', 'url': 'dashboard_home'},
                {'name': 'Demandes de souscription', 'url': 'liste_demandes_souscription'},
                {'name': 'Affecter demande', 'url': None},
            ],
        })
    
@staff_member_required
def liste_demandes_souscription(request):
    statut = request.GET.get('statut')
    demandes = DemandeSouscription.objects.all()

    if statut == 'acceptee':
        demandes = demandes.filter(statut='affectée')
    elif statut == 'en_attente':
        demandes = demandes.filter(statut='en_attente')
    elif statut == 'refusee':
        demandes = demandes.filter(statut='refusée')

    context = {
        'demandes': demandes,
        'statut': statut,
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Demandes de souscription', 'url': None},
        ]
    }
    return render(request, 'souscriptions/liste_demandes_souscription.html', context)

def demande_souscription_detail(request, demande_id):
    # demande = get_object_or_404(DemandeSouscription, id=demande_id)
    # souscription = get_object_or_404(Souscription, souscripteur=demande.souscripteur, statut='active')
    demande = DemandeSouscription.objects.filter(id=demande_id).first()
    souscription = None
    if demande and demande.statut == 'affectée':
        souscription = Souscription.objects.filter(
            souscripteur=demande.souscripteur,
            statut='active'
        ).first()
    # Breadcrumb dynamique selon le rôle
    if request.user.role == 'parent':
        breadcrumb = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Mes demandes de souscriptions', 'url': 'dashboard_home'},  # Pas de lien cliquable pour le parent
            {'name': 'Détails de la demande', 'url': None},
        ]
    else:  # Superuser ou autre rôle admin
        breadcrumb = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Demandes de souscription', 'url': 'liste_demandes_souscription'},
            {'name': 'Détails de la demande', 'url': None},
        ]

    context = {
        'demande': demande,
        'breadcrumb': breadcrumb,
        'souscription': souscription,
    }
    return render(request, 'souscriptions/demande_souscription_detail.html', context)

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

