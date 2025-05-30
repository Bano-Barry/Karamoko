from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from core.forms import NiveauForm
from paiements.models import OffreTarifaire
from .models import Niveau
from repetiteurs.models import Cours, Repetiteur

def home(request):
    return render(request, 'vitrine/home.html')

def encadreurs(request):
    repetiteurs = Repetiteur.objects.all()
    return render(request, 'vitrine/encadreurs.html', {'repetiteurs': repetiteurs})

def services(request):
    return render(request, 'vitrine/services.html')

def about(request):
    return render(request, 'vitrine/about.html')

def guide_parent(request):
    return render(request, 'vitrine/guide_parent.html')
def guide_repetiteur(request):
    return render(request, 'vitrine/guide_repetiteur.html')


# Liste des niveaux
class NiveauListView(ListView):
    model = Niveau
    template_name = 'core/niveau_list.html'
    context_object_name = 'niveaux'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': None},
        ]
        return context

# Création d'un niveau
class NiveauCreateView(CreateView):
    model = Niveau
    template_name = 'core/niveau_form.html'
    form_class = NiveauForm
    success_url = reverse_lazy('niveau_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': 'niveau_list'},
            {'name': 'Créer', 'url': None},
        ]
        return context

# Mise à jour d'un niveau
class NiveauUpdateView(UpdateView):
    model = Niveau
    template_name = 'core/niveau_form.html'
    form_class = NiveauForm
    success_url = reverse_lazy('niveau_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': 'niveau_list'},
            {'name': 'Modifier', 'url': None},
        ]
        return context

# Suppression d'un niveau
class NiveauDeleteView(DeleteView):
    model = Niveau
    template_name = 'core/niveau_confirm_delete.html'
    success_url = reverse_lazy('niveau_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Dashboard', 'url': 'dashboard_home'},
            {'name': 'Niveaux', 'url': 'niveau_list'},
            {'name': 'Supprimer', 'url': None},
        ]
        return context

# urls.py
# Ajout d'une vue pour tester le 404
def trigger_404(request):
    return render(request, 'vitrine/404.html', status=404)
handler404 = trigger_404

@require_http_methods(["GET"])
def ajax_matieres_par_niveau(request, niveau_id):
    """
    Retourne les matières/cours disponibles pour un niveau donné
    GET /ajax/matieres-par-niveau/<int:niveau_id>/
    """
    try:
        niveau = get_object_or_404(Niveau, id=niveau_id)
        
        # Récupérer tous les cours pour ce niveau
        cours_queryset = niveau.cours.all().order_by('titre')
        
        # Préparer les données JSON
        matieres_data = []
        for cours in cours_queryset:
            matieres_data.append({
                'id': cours.id,
                'titre': cours.titre,
                'description': cours.description or '',
            })
        
        return JsonResponse({
            'success': True,
            'niveau': {
                'id': niveau.id,
                'nom': niveau.nom
            },
            'matieres': matieres_data,
            'count': len(matieres_data)
        })
        
    except Niveau.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Niveau non trouvé'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt  # Géré par le header X-CSRFToken dans le JS
def ajax_offres_par_niveau(request, niveau_id):
    """
    Retourne les offres tarifaires compatibles avec un niveau et des matières
    POST /ajax/offres-par-niveau/<int:niveau_id>/
    Body: {"matieres": [1, 2, 3]}
    """
    try:
        niveau = get_object_or_404(Niveau, id=niveau_id)
        
        # Récupérer les matières sélectionnées depuis le POST
        try:
            data = json.loads(request.body)
            matieres_ids = data.get('matieres', [])
            matieres_ids = [int(m_id) for m_id in matieres_ids]  # S'assurer que ce sont des entiers
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({
                'success': False,
                'error': 'Données POST invalides'
            }, status=400)
        
        # Vérifier que les matières existent et sont compatibles avec le niveau
        matieres_selectionnees = Cours.objects.filter(
            id__in=matieres_ids,
            niveaux=niveau
        )
        
        if len(matieres_selectionnees) != len(matieres_ids):
            return JsonResponse({
                'success': False,
                'error': 'Certaines matières ne sont pas compatibles avec ce niveau'
            }, status=400)
        
        # Récupérer les offres compatibles avec ce niveau
        offres_queryset = OffreTarifaire.objects.filter(
            niveaux=niveau,
            is_active=True
        ).order_by('ordre', 'prix_unitaire')
        
        # Préparer les données des offres avec prix calculés
        offres_data = []
        nombre_matieres = len(matieres_ids)
        
        for offre in offres_queryset:
            # Calculer le prix selon le nombre de matières
            prix_calcule = offre.get_prix_pour_matieres(nombre_matieres)
            
            # Vérifier si cette offre est pertinente pour les matières sélectionnées
            offre_pertinente = True
            
            # Si l'offre a des matières spécifiques, vérifier la compatibilité
            if offre.matieres_incluses.exists():
                matieres_offre = set(offre.matieres_incluses.values_list('id', flat=True))
                matieres_demandees = set(matieres_ids)
                
                # Pour les forfaits globaux, toutes les matières doivent être incluses
                if offre.type_offre == 'forfait_global':
                    offre_pertinente = matieres_demandees.issubset(matieres_offre)
                # Pour les autres, au moins une matière doit correspondre
                else:
                    offre_pertinente = bool(matieres_demandees.intersection(matieres_offre))
            
            if offre_pertinente:
                offres_data.append({
                    'id': offre.id,
                    'nom': offre.nom,
                    'description': offre.description or '',
                    'type_offre': offre.type_offre,
                    'type_offre_display': offre.get_type_offre_display(),
                    'prix_unitaire': offre.prix_unitaire,
                    'prix_calcule': prix_calcule,
                    'nombre_seances_mois': offre.nombre_seances_mois,
                    'duree_seance_max': offre.duree_seance_max,
                    'jours_par_semaine': offre.jours_par_semaine,
                    'matieres_incluses': list(offre.matieres_incluses.values_list('titre', flat=True)) if offre.matieres_incluses.exists() else []
                })
        
        return JsonResponse({
            'success': True,
            'niveau': {
                'id': niveau.id,
                'nom': niveau.nom
            },
            'matieres_selectionnees': list(matieres_selectionnees.values('id', 'titre')),
            'nombre_matieres': nombre_matieres,
            'offres': offres_data,
            'count': len(offres_data)
        })
        
    except Niveau.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Niveau non trouvé'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)


# Vue bonus : pour débugger et tester
@require_http_methods(["GET"])
def ajax_debug_niveau(request, niveau_id):
    """
    Vue de debug pour voir la structure complète d'un niveau
    GET /ajax/debug-niveau/<int:niveau_id>/
    """
    try:
        niveau = get_object_or_404(Niveau, id=niveau_id)
        
        return JsonResponse({
            'niveau': {
                'id': niveau.id,
                'nom': niveau.nom,
                'ordre': niveau.ordre
            },
            'cours_disponibles': list(niveau.cours.values('id', 'titre', 'description')),
            'offres_disponibles': list(niveau.offres_tarifaires.filter(is_active=True).values(
                'id', 'nom', 'type_offre', 'prix_unitaire', 'nombre_seances_mois'
            ))
        })
        
    except Niveau.DoesNotExist:
        return JsonResponse({'error': 'Niveau non trouvé'}, status=404)
