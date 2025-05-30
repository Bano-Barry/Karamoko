from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta

from souscriptions.models import DemandeSouscription, Souscription
from repetiteurs.models import Repetiteur

@login_required
def dashboard_home(request):
    user = request.user
    context = {}

    if user.role == 'repetiteur':
        context['dashboard_type'] = 'repetiteur'
        repetiteur = user.repetiteur
        souscriptions = Souscription.objects.filter(repetiteur=repetiteur)
        context['souscriptions'] = souscriptions

    elif user.role == 'parent':
        context['dashboard_type'] = 'parent'
        demandes = DemandeSouscription.objects.filter(souscripteur__user=user)
        context['demandes'] = demandes

    elif user.is_superuser:
        context['dashboard_type'] = 'admin'
        
        # Statistiques générales pour l'admin
        context.update(get_admin_statistics())
        
        # Alertes pour l'admin
        context['alertes'] = get_admin_alerts()
        
    return render(request, 'dashboard/home.html', context)


def get_admin_statistics():
    """Récupère toutes les statistiques pour le dashboard admin"""
    today = timezone.now().date()
    
    # Nombre total de souscriptions
    total_souscriptions = Souscription.objects.count()
    
    # Demandes en attente
    demandes_en_attente = DemandeSouscription.objects.filter(
        statut='en_attente'
    ).count()
    
    # Répétiteurs actifs (ayant au moins une souscription active)
    repetiteurs_actifs = Repetiteur.objects.filter(
        souscriptions__statut='active'
    ).distinct().count()
    
    # Montant total encaissé (basé sur les souscriptions actives)
    # Vous devrez adapter selon votre modèle de prix
    souscriptions_actives = Souscription.objects.filter(statut='active')
    montant_total = 0
    for souscription in souscriptions_actives:
        if souscription.offre_tarifaire:
            # Calculer le prix selon le nombre de matières
            nombre_matieres = souscription.cours.count()
            prix = souscription.offre_tarifaire.get_prix_pour_matieres(nombre_matieres)
            montant_total += prix
    
    # Données pour le graphique d'évolution (6 derniers mois)
    chart_data = get_subscription_evolution_data()
    
    return {
        'total_souscriptions': total_souscriptions,
        'demandes_en_attente': demandes_en_attente,
        'repetiteurs_actifs': repetiteurs_actifs,
        'montant_total': montant_total,
        'chart_data': chart_data,
    }


def get_subscription_evolution_data():
    """Génère les données pour le graphique d'évolution des souscriptions"""
    today = timezone.now().date()
    six_months_ago = today - timedelta(days=180)
    
    # Grouper les souscriptions par mois sur les 6 derniers mois
    monthly_data = []
    
    for i in range(6):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        souscriptions_count = Souscription.objects.filter(
            date_creation__date__range=[month_start, month_end]
        ).count()
        
        monthly_data.insert(0, {
            'month': month_start.strftime('%B %Y'),
            'count': souscriptions_count
        })
    
    return monthly_data


def get_admin_alerts():
    """Génère les alertes pour l'administrateur"""
    alerts = []
    
    # Alertes pour demandes en attente depuis plus de 3 jours
    three_days_ago = timezone.now() - timedelta(days=3)
    demandes_anciennes = DemandeSouscription.objects.filter(
        statut='en_attente',
        date_demande__lt=three_days_ago
    ).count()
    
    if demandes_anciennes > 0:
        alerts.append(f"{demandes_anciennes} demande(s) en attente depuis plus de 3 jours")
    
    # Alertes pour répétiteurs sans souscriptions actives
    repetiteurs_inactifs = Repetiteur.objects.filter(
        is_soumis=True
    ).exclude(
        souscriptions__statut='active'
    ).count()
    
    if repetiteurs_inactifs > 0:
        alerts.append(f"{repetiteurs_inactifs} répétiteur(s) validé(s) sans souscriptions actives")
    
    # Alertes pour souscriptions expirant bientôt (dans 7 jours)
    seven_days_later = timezone.now().date() + timedelta(days=7)
    souscriptions_expirant = Souscription.objects.filter(
        statut='active',
        date_fin__lte=seven_days_later
    ).count()
    
    if souscriptions_expirant > 0:
        alerts.append(f"{souscriptions_expirant} souscription(s) expirent dans les 7 prochains jours")
    
    # Alertes pour répétiteurs en attente de validation
    repetiteurs_en_attente = Repetiteur.objects.filter(
        is_soumis=False
    ).count()
    
    if repetiteurs_en_attente > 0:
        alerts.append(f"{repetiteurs_en_attente} répétiteur(s) en attente de validation")
    
    return alerts


# Vue supplémentaire pour les données AJAX du graphique
@login_required
def dashboard_chart_data(request):
    """API pour récupérer les données du graphique via AJAX"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    
    chart_data = get_subscription_evolution_data()
    return JsonResponse(chart_data, safe=False)