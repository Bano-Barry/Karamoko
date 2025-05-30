# management/commands/create_test_data.py

from django.core.management.base import BaseCommand
from paiements.models import OffreTarifaire
from repetiteurs.models import Niveau, Cours

def create_test_data():
    """Crée des données de test pour le système de souscription"""
    
    print("Création des données de test...")
    
    # 1. CRÉER LES NIVEAUX
    niveaux_data = [
        {'nom': '1ère année', 'ordre': 1},
        {'nom': '2ème année', 'ordre': 2},
        {'nom': '3ème année', 'ordre': 3},
        {'nom': '4ème année', 'ordre': 4},
        {'nom': '5ème année', 'ordre': 5},
        {'nom': '6ème année', 'ordre': 6},
        {'nom': '7ème année', 'ordre': 7},
        {'nom': '8ème année', 'ordre': 8},
        {'nom': '9ème année', 'ordre': 9},
        {'nom': '10ème année', 'ordre': 10},
        {'nom': '11ème année', 'ordre': 11},
        {'nom': '12ème année', 'ordre': 12},
    ]
    
    niveaux = {}
    for niveau_data in niveaux_data:
        niveau, created = Niveau.objects.get_or_create(
            nom=niveau_data['nom'],
            defaults={'ordre': niveau_data['ordre']}
        )
        niveaux[niveau_data['nom']] = niveau
        if created:
            print(f"✅ Niveau créé: {niveau.nom}")
    
    # 2. CRÉER LES COURS/MATIÈRES
    cours_data = {
        # Primaire (1ère-5ème)
        'Français': ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année'],
        'Mathématiques': ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année'],
        'Sciences': ['3ème année', '4ème année', '5ème année'],
        'Histoire-Géographie': ['4ème année', '5ème année'],
        
        # Collège (6ème-9ème)
        'Français': ['6ème année', '7ème année', '8ème année', '9ème année'],
        'Mathématiques': ['6ème année', '7ème année', '8ème année', '9ème année'],
        'Sciences Physiques': ['6ème année', '7ème année', '8ème année', '9ème année'],
        'Sciences de la Vie et de la Terre': ['6ème année', '7ème année', '8ème année', '9ème année'],
        'Histoire-Géographie': ['6ème année', '7ème année', '8ème année', '9ème année'],
        'Anglais': ['6ème année', '7ème année', '8ème année', '9ème année'],
        
        # Lycée (10ème-12ème)
        'Mathématiques': ['10ème année', '11ème année', '12ème année'],
        'Physique': ['10ème année', '11ème année', '12ème année'],
        'Chimie': ['10ème année', '11ème année', '12ème année'],
        'Biologie': ['11ème année', '12ème année'],
        'Français': ['10ème année', '11ème année', '12ème année'],
        'Philosophie': ['11ème année', '12ème année'],
        'Histoire-Géographie': ['10ème année', '11ème année', '12ème année'],
        'Anglais': ['10ème année', '11ème année', '12ème année'],
    }
    
    cours_objects = {}
    for titre, niveaux_liste in cours_data.items():
        cours, created = Cours.objects.get_or_create(
            titre=titre,
            defaults={'description': f'Cours de {titre}'}
        )
        cours_objects[titre] = cours
        
        # Associer aux niveaux
        for niveau_nom in niveaux_liste:
            if niveau_nom in niveaux:
                cours.niveaux.add(niveaux[niveau_nom])
        
        if created:
            print(f"✅ Cours créé: {cours.titre}")
    
    # 3. CRÉER LES OFFRES TARIFAIRES
    offres_data = [
        # PRIMAIRE - Forfait global
        {
            'nom': 'Forfait Primaire Complet',
            'description': 'Toutes les matières du primaire incluses',
            'type_offre': 'forfait_global',
            'prix_unitaire': 150000,  # 150k GNF
            'niveaux': ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année'],
            'matieres': ['Français', 'Mathématiques', 'Sciences', 'Histoire-Géographie'],
            'nombre_seances_mois': 12,
            'duree_seance_max': 120,  # 2h
            'jours_par_semaine': 3,
        },
        
        # COLLÈGE - Par matière
        {
            'nom': 'Collège - Par Matière',
            'description': 'Tarif unitaire par matière pour le collège',
            'type_offre': 'par_matiere',
            'prix_unitaire': 80000,  # 80k GNF par matière
            'niveaux': ['6ème année', '7ème année', '8ème année', '9ème année'],
            'matieres': ['Français', 'Mathématiques', 'Sciences Physiques', 'Sciences de la Vie et de la Terre', 'Histoire-Géographie', 'Anglais'],
            'nombre_seances_mois': 8,
            'duree_seance_max': 180,  # 3h
            'jours_par_semaine': 2,
        },
        
        # LYCÉE 10ème - Pack Examen (Maths + Physique + Chimie)
        {
            'nom': 'Pack Examen 10ème',
            'description': 'Pack spécial Maths + Physique + Chimie pour la 10ème',
            'type_offre': 'pack_examen',
            'prix_unitaire': 100000,  # Prix unitaire
            'prix_combine': 250000,   # Prix combiné pour les 3 matières
            'niveaux': ['10ème année'],
            'matieres': ['Mathématiques', 'Physique', 'Chimie'],
            'nombre_seances_mois': 12,
            'duree_seance_max': 180,
            'jours_par_semaine': 3,
        },
        
        # LYCÉE 11-12ème - Par matière
        {
            'nom': 'Lycée Supérieur - Par Matière',
            'description': 'Tarif par matière pour 11ème et 12ème',
            'type_offre': 'par_matiere',
            'prix_unitaire': 120000,  # 120k GNF par matière
            'niveaux': ['11ème année', '12ème année'],
            'matieres': ['Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Français', 'Philosophie', 'Histoire-Géographie', 'Anglais'],
            'nombre_seances_mois': 10,
            'duree_seance_max': 180,
            'jours_par_semaine': 2,
        },
        
        # LYCÉE 11-12ème - Pack Spécialité Sciences
        {
            'nom': 'Pack Spécialité Sciences',
            'description': 'Pack Maths + Physique + Chimie + Biologie',
            'type_offre': 'pack_specialite',
            'prix_unitaire': 400000,  # Prix fixe pour le pack
            'niveaux': ['11ème année', '12ème année'],
            'matieres': ['Mathématiques', 'Physique', 'Chimie', 'Biologie'],
            'nombre_seances_mois': 16,
            'duree_seance_max': 240,  # 4h
            'jours_par_semaine': 4,
        }
    ]
    
    for i, offre_data in enumerate(offres_data):
        offre, created = OffreTarifaire.objects.get_or_create(
            nom=offre_data['nom'],
            defaults={
                'description': offre_data['description'],
                'type_offre': offre_data['type_offre'],
                'prix_unitaire': offre_data['prix_unitaire'],
                'prix_combine': offre_data.get('prix_combine'),
                'nombre_seances_mois': offre_data['nombre_seances_mois'],
                'duree_seance_max': offre_data['duree_seance_max'],
                'jours_par_semaine': offre_data['jours_par_semaine'],
                'ordre': i,
                'is_active': True,
            }
        )
        
        # Associer aux niveaux
        for niveau_nom in offre_data['niveaux']:
            if niveau_nom in niveaux:
                offre.niveaux.add(niveaux[niveau_nom])
        
        # Associer aux matières
        for matiere_nom in offre_data['matieres']:
            if matiere_nom in cours_objects:
                offre.matieres_incluses.add(cours_objects[matiere_nom])
        
        if created:
            print(f"✅ Offre créée: {offre.nom} - {offre.prix_unitaire:,} GNF")
    
    print("\n🎉 Données de test créées avec succès!")
    print(f"📊 Résumé:")
    print(f"   - {Niveau.objects.count()} niveaux")
    print(f"   - {Cours.objects.count()} cours")
    print(f"   - {OffreTarifaire.objects.count()} offres tarifaires")


# Si c'est une commande de management
class Command(BaseCommand):
    help = 'Crée des données de test pour le système de souscription'
    
    def handle(self, *args, **options):
        create_test_data()

# Si vous l'exécutez directement dans le shell :
# python manage.py shell
# >>> exec(open('create_test_data.py').read())