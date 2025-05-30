from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

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
# details d'une souscription
class SouscriptionDetailView(DetailView):
    model = Souscription
    template_name = 'souscriptions/souscription_detail.html'
    context_object_name = 'souscription'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Souscriptions', 'url': 'souscription_list'},
            {'name': 'Détails', 'url': None},
        ]
        return context
    
@login_required
def affecter_demande_souscription(request, demande_id):
    """
    Affecte un répétiteur à une demande de souscription et crée la souscription correspondante
    """
    demande = get_object_or_404(DemandeSouscription, id=demande_id, statut='en_attente')
    
    # Filtrer les répétiteurs validés et potentiellement compatibles
    repetiteurs_disponibles = Repetiteur.objects.filter(
        user__is_validated=True,
        user__is_active=True
    ).select_related('user').prefetch_related('cours')
    
    # Filtrer par compatibilité avec les matières demandées
    matieres_demandees = demande.matieres.all()
    repetiteurs_compatibles = []
    
    for repetiteur in repetiteurs_disponibles:
        # Vérifier si le répétiteur maîtrise au moins une des matières demandées
        if repetiteur.cours.filter(id__in=matieres_demandees.values_list('id', flat=True)).exists():
            repetiteurs_compatibles.append(repetiteur)
    
    if request.method == 'POST':
        repetiteur_id = request.POST.get('repetiteur')
        
        if not repetiteur_id:
            messages.error(request, "Veuillez sélectionner un répétiteur.")
            return render(request, 'souscriptions/affecter_demande.html', {
                'demande': demande,
                'repetiteurs': repetiteurs_compatibles
            })
        
        repetiteur = get_object_or_404(Repetiteur, id=repetiteur_id)
        
        # Vérification de compatibilité
        if not repetiteur.cours.filter(id__in=matieres_demandees.values_list('id', flat=True)).exists():
            messages.error(request, "Ce répétiteur ne maîtrise aucune des matières demandées.")
            return render(request, 'souscriptions/affecter_demande.html', {
                'demande': demande,
                'repetiteurs': repetiteurs_compatibles
            })
        
        # Validation de l'offre tarifaire
        if not demande.offre_tarifaire:
            messages.error(request, "La demande n'a pas d'offre tarifaire définie.")
            return render(request, 'souscriptions/affecter_demande.html', {
                'demande': demande,
                'repetiteurs': repetiteurs_compatibles
            })
        
        try:
            with transaction.atomic():
                # Calcul de la durée selon l'offre tarifaire
                duree_mois = demande.offre_tarifaire.duree_mois if hasattr(demande.offre_tarifaire, 'duree_mois') else 1
                date_debut = timezone.now().date()
                date_fin = date_debut + timedelta(days=duree_mois * 30)  # Approximation
                
                # Calcul du nombre de séances prévues
                # Assumons 4 séances par mois par matière (à adapter selon votre logique)
                nombre_matieres = demande.matieres.count()
                seances_prevues = nombre_matieres * duree_mois * 4
                
                # Création de la souscription
                souscription = Souscription.objects.create(
                    souscripteur=demande.souscripteur,
                    repetiteur=repetiteur,
                    offre_tarifaire=demande.offre_tarifaire,
                    moyen_paiement=demande.moyen_paiement,
                    date_debut=date_debut,
                    date_fin=date_fin,
                    statut='active',
                    seances_prevues=seances_prevues,
                    seances_effectuees=0,
                    cree_par=request.user,
                    demande_origine=demande
                )
                
                # Association des matières
                souscription.cours.set(demande.matieres.all())
                
                # Mise à jour de la demande
                demande.statut = 'affectée'
                demande.date_traitement = timezone.now()
                demande.traite_par = request.user
                demande.save()
                
                messages.success(
                    request, 
                    f"✅ Demande affectée avec succès à {repetiteur.user.first_name} {repetiteur.user.last_name}. "
                    f"Souscription créée du {date_debut} au {date_fin}."
                )
                
                return redirect('liste_demandes_souscription')
                
        except Exception as e:
            messages.error(request, f"Erreur lors de la création de la souscription : {str(e)}")
    
    # Calcul du coût estimé pour affichage
    cout_estime = demande.cout_total_estime
    
    context = {
        'demande': demande,
        'repetiteurs': repetiteurs_compatibles,
        'cout_estime': cout_estime,
        'matieres_demandees': matieres_demandees,
        'breadcrumb': [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Demandes', 'url': 'liste_demandes_souscription'},
            {'name': 'Affecter', 'url': None},
        ]
    }

    return render(request, 'souscriptions/affecter_demande_souscription.html', context)

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

