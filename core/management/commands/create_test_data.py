# management/commands/create_test_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from paiements.models import OffreTarifaire, MethodePaiement
from repetiteurs.models import Niveau, Cours, Repetiteur
from django.core.files.uploadedfile import SimpleUploadedFile

from souscripteurs.models import Souscripteur

User = get_user_model()

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
    tous_les_cours = [
        # primaire 
        'Dictée', 
        'Rédaction',
        'Calcul Ecrit', 
        'SVT',
        'Histoire', 
        'Géographie',
        'Education Civique et Morale',
        # collège
        'Mathématiques', 
        'Physique',
        'Chimie',
        'Français',
        'Anglais',
        'Biologie',
        'Histoire',
        'Géographie',
        # lycée
        'Economie',
        'Philosophie'
    ]
    
    cours_objects = {}
    for titre_cours in tous_les_cours:
        cours, created = Cours.objects.get_or_create(
            titre=titre_cours,
            defaults={'description': f'Cours de {titre_cours}'}
        )
        cours_objects[titre_cours] = cours
        if created:
            print(f"✅ Cours créé: {cours.titre}")
    
    # 3. ASSOCIER LES COURS AUX NIVEAUX
    cours_niveaux_mapping = [
        # PRIMAIRE
        ('Dictée', ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année']),
        ('Rédaction', ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année']),
        ('Calcul Ecrit', ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année']),
        ('SVT', ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année']),
        ('Histoire', ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année']),
        ('Géographie', ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année']),
        ('Education Civique et Morale', ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année']),
        # COLLÈGE
        ('Français', ['7ème année', '8ème année', '9ème année', '10ème année']),
        ('Anglais', ['6ème année', '7ème année', '8ème année', '9ème année', '10ème année']),
        ('Mathématiques', ['7ème année', '8ème année', '9ème année', '10ème année']),
        ('Physique', ['7ème année', '8ème année', '9ème année', '10ème année']),
        ('Chimie', ['7ème année', '8ème année', '9ème année', '10ème année']),
        ('Biologie', ['7ème année', '8ème année', '9ème année', '10ème année']),
        ('Histoire', ['7ème année', '8ème année', '9ème année', '10ème année']),
        ('Géographie', ['7ème année', '8ème année', '9ème année', '10ème année']),
        # LYCÉE
        ('Mathématiques', ['11ème année', '12ème année']),
        ('Physique', ['11ème année', '12ème année']),
        ('Chimie', ['11ème année', '12ème année']),
        ('Français', ['11ème année', '12ème année']),
        ('Anglais', ['10ème année', '11ème année', '12ème année']),
        ('Biologie', ['11ème année', '12ème année']),
        ('Philosophie', ['11ème année', '12ème année']),
        ('Histoire', ['11ème année', '12ème année']),
        ('Géographie', ['11ème année', '12ème année']),
    ]
    
    # Associer cours et niveaux
    for titre_cours, niveaux_liste in cours_niveaux_mapping:
        cours = cours_objects[titre_cours]
        for niveau_nom in niveaux_liste:
            if niveau_nom in niveaux:
                cours.niveaux.add(niveaux[niveau_nom])
                print(f"✅ {titre_cours} associé au niveau {niveau_nom}")
    
    # 4. CRÉER LES MÉTHODES DE PAIEMENT
    methodes_paiement_data = [
        {'nom': 'Orange Money', 'description': 'Paiement via Orange Money'},
        {'nom': 'MTN Mobile Money', 'description': 'Paiement via MTN Mobile Money'},
        {'nom': 'Moov Money', 'description': 'Paiement via Moov Money'},
        {'nom': 'Espèces', 'description': 'Paiement en espèces'},
        {'nom': 'Virement bancaire', 'description': 'Virement bancaire local'},
    ]
    
    methodes_paiement = {}
    for methode_data in methodes_paiement_data:
        methode, created = MethodePaiement.objects.get_or_create(
            nom=methode_data['nom'],
            defaults={'description': methode_data['description']}
        )
        methodes_paiement[methode_data['nom']] = methode
        if created:
            print(f"✅ Méthode de paiement créée: {methode.nom}")
    
    # 5. CRÉER LES OFFRES TARIFAIRES
    offres_data = [
        # PRIMAIRE - Forfait global
        {
            'nom': 'Forfait Primaire Complet',
            'description': 'Toutes les matières du primaire incluses',
            'type_offre': 'forfait_global',
            'prix_unitaire': 500000,  # 500k GNF
            'niveaux': ['1ère année', '2ème année', '3ème année', '4ème année', '5ème année', '6ème année'],
            'matieres': ['Dictée', 'Rédaction', 'Calcul Ecrit', 'SVT', 'Histoire', 'Géographie', 'Education Civique et Morale'],
            'nombre_seances_mois': 12,
            'duree_seance_max': 120,  # 2h
            'jours_par_semaine': 4,
        },
        
        # COLLÈGE - Par matière
        {
            'nom': 'Collège - Par Matière',
            'description': 'Tarif unitaire par matière pour le collège',
            'type_offre': 'par_matiere',
            'prix_unitaire': 200000,  # 200k GNF par matière
            'niveaux': ['7ème année', '8ème année', '9ème année'],
            'matieres': ['Français', 'Anglais', 'Mathématiques', 'Physique', 'Chimie', 'Histoire', 'Géographie', 'Biologie'],
            'nombre_seances_mois': 12,
            'duree_seance_max': 180,  # 3h
            'jours_par_semaine': 3,
        },
        
        # 10ème - Pack Examen
        {
            'nom': 'Pack Examen 10ème',
            'description': 'Pack spécial Maths + Physique + Chimie pour la 10ème + autre matière',
            'type_offre': 'pack_examen',
            'prix_unitaire': 100000,  # Prix unitaire
            'prix_combine': 350000,   # Prix combiné pour les 3 matières
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
            'prix_unitaire': 200000,  # 200k GNF par matière
            'niveaux': ['11ème année', '12ème année'],
            'matieres': ['Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Français', 'Philosophie', 'Histoire', 'Géographie', 'Anglais', 'Economie'],
            'nombre_seances_mois': 12,
            'duree_seance_max': 180,
            'jours_par_semaine': 3,
        },
        
        # LYCÉE 11-12ème - Pack Sciences
        {
            'nom': 'Pack Spécialité Sciences',
            'description': 'Pack Maths + Physique + Chimie + Biologie',
            'type_offre': 'pack_specialite',
            'prix_unitaire': 400000,  # Prix fixe pour le pack
            'niveaux': ['11ème année', '12ème année'],
            'matieres': ['Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Français'],
            'nombre_seances_mois': 12,
            'duree_seance_max': 180,  # 3h
            'jours_par_semaine': 3,
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
    
    # 6. CRÉER DES UTILISATEURS PARENTS/SOUSCRIPTEURS
    prenoms_hommes = ['Amadou', 'Mamadou', 'Alpha', 'Ibrahima', 'Ousmane', 'Sekou', 'Mohamed', 'Thierno', 'Boubacar', 'Aboubacar', 'Saliou', 'Elhadj', 'Lansana', 'Fodé', 'Facinet']
    prenoms_femmes = ['Fatoumata', 'Aissatou', 'Mariama', 'Kadiatou', 'Aminata', 'Hawa', 'Ramata', 'Nènè', 'Mabinty', 'Safiatou', 'Hadja', 'Binta', 'Fanta', 'Coumba', 'Oumou']
    noms_famille = ['Diallo', 'Barry', 'Bah', 'Camara', 'Conde', 'Souare', 'Keita', 'Toure', 'Cisse', 'Kone', 'Traore', 'Sylla', 'Bangoura', 'Doumbouya', 'Sangare', 'Fofana', 'Soumah', 'Cherif', 'Dioubate', 'Sidibe']
    zones_conakry = ['Kaloum', 'Dixinn', 'Matam', 'Ratoma', 'Matoto', 'Kipé', 'Lambandji', 'Taouyah', 'Madina', 'Hamdallaye', 'Koloma', 'Sonfonia', 'Bambeto', 'Cosa', 'Minière', 'Belle-vue', 'Almamya', 'Sandervalia', 'Coronthie', 'Kaporo Rails']
    
    # Générer des numéros de téléphone guinéens
    def generer_numero_guineen():
        prefixes = ['622', '623', '624', '625', '626', '627', '628', '629', '655', '656', '657', '664', '665', '666', '667', '669']
        return f"{random.choice(prefixes)}{random.randint(100000, 999999)}"
    
    parents = []
    for i in range(20):  # Créer 20 parents
        prenom = random.choice(prenoms_hommes + prenoms_femmes)
        nom = random.choice(noms_famille)
        phone = generer_numero_guineen()
        adresse = f"{random.choice(zones_conakry)}, Conakry"
        
        # Vérifier que le numéro n'existe pas déjà
        while User.objects.filter(phone=phone).exists():
            phone = generer_numero_guineen()
        
        parent_user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': prenom,
                'last_name': nom,
                'role': 'parent',
                'adresse': adresse,
                'is_validated': True,
            }
        )
        parent_user.set_password('karamoko')
        parent_user.save()
        
        # Créer le profil souscripteur
        souscripteur, created = Souscripteur.objects.get_or_create(
            user=parent_user,
            defaults={
                'cgu_acceptees': True,
            }
        )
        
        parents.append(parent_user)
        if created:
            print(f"✅ Parent créé: {parent_user.first_name} {parent_user.last_name} ({parent_user.phone})")
    
    # 7. CRÉER DES RÉPÉTITEURS
    def create_dummy_file(filename, content="Contenu du fichier test"):
        """Crée un fichier factice pour les tests"""
        return SimpleUploadedFile(filename, content.encode('utf-8'))

    repetiteurs = []

    # 5 encadrants primaire
    matieres_primaire = ['Dictée', 'Rédaction', 'Calcul Ecrit', 'SVT', 'Histoire', 'Géographie', 'Education Civique et Morale']
    for i in range(5):
        prenom = random.choice(prenoms_hommes + prenoms_femmes)
        nom = random.choice(noms_famille)
        phone = generer_numero_guineen()
        adresse = f"{random.choice(zones_conakry)}, Conakry"
        while User.objects.filter(phone=phone).exists():
            phone = generer_numero_guineen()
        repetiteur_user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': prenom,
                'last_name': nom,
                'role': 'repetiteur',
                'adresse': adresse,
                'is_validated': True,
            }
        )
        repetiteur_user.set_password('karamoko')
        repetiteur_user.save()
        repetiteur, created = Repetiteur.objects.get_or_create(
            user=repetiteur_user,
            defaults={
                'biographie': "Encadrant toutes matières du primaire.",
                'experience': random.randint(5, 20),
                'prix_par_seance': 200000,
                'disponibilite_matin': True,
                'disponibilite_apres_midi': True,
                'disponibilite_soir': True,
                'disponibilite_weekend': True,
                'is_soumis': True,
                'cgu_acceptees': True,
                'avatar': create_dummy_file(f"avatar_primaire_{i}.jpg", "Image avatar"),
                'piece_identite': create_dummy_file(f"carte_id_primaire_{i}.pdf", "Carte d'identité"),
                'diplome': create_dummy_file(f"diplome_primaire_{i}.pdf", "Diplôme universitaire"),
                'contrat_ecole': create_dummy_file(f"contrat_primaire_{i}.pdf", "Contrat école"),
            }
        )
        cours_selectionnes = [cours_objects[m] for m in matieres_primaire if m in cours_objects]
        repetiteur.cours.set(cours_selectionnes)
        repetiteurs.append(repetiteur_user)
        print(f"✅ Répétiteur PRIMAIRE créé: {repetiteur_user.first_name} {repetiteur_user.last_name} ({repetiteur_user.phone})")

    # 5 encadrants collège
    matieres_college = ['Français', 'Anglais', 'Mathématiques', 'Physique', 'Chimie', 'Histoire', 'Géographie', 'Biologie']
    for i in range(5):
        prenom = random.choice(prenoms_hommes + prenoms_femmes)
        nom = random.choice(noms_famille)
        phone = generer_numero_guineen()
        adresse = f"{random.choice(zones_conakry)}, Conakry"
        while User.objects.filter(phone=phone).exists():
            phone = generer_numero_guineen()
        repetiteur_user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': prenom,
                'last_name': nom,
                'role': 'repetiteur',
                'adresse': adresse,
                'is_validated': True,
            }
        )
        repetiteur_user.set_password('karamoko')
        repetiteur_user.save()
        repetiteur, created = Repetiteur.objects.get_or_create(
            user=repetiteur_user,
            defaults={
                'biographie': "Encadrant toutes matières du collège.",
                'experience': random.randint(5, 20),
                'prix_par_seance': 250000,
                'disponibilite_matin': True,
                'disponibilite_apres_midi': True,
                'disponibilite_soir': True,
                'disponibilite_weekend': True,
                'is_soumis': True,
                'cgu_acceptees': True,
                'avatar': create_dummy_file(f"avatar_college_{i}.jpg", "Image avatar"),
                'piece_identite': create_dummy_file(f"carte_id_college_{i}.pdf", "Carte d'identité"),
                'diplome': create_dummy_file(f"diplome_college_{i}.pdf", "Diplôme universitaire"),
                'contrat_ecole': create_dummy_file(f"contrat_college_{i}.pdf", "Contrat école"),
            }
        )
        cours_selectionnes = [cours_objects[m] for m in matieres_college if m in cours_objects]
        repetiteur.cours.set(cours_selectionnes)
        repetiteurs.append(repetiteur_user)
        print(f"✅ Répétiteur COLLÈGE créé: {repetiteur_user.first_name} {repetiteur_user.last_name} ({repetiteur_user.phone})")

    # 5 encadrants lycée
    matieres_lycee = ['Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Français', 'Philosophie', 'Histoire', 'Géographie', 'Anglais', 'Economie']
    for i in range(5):
        prenom = random.choice(prenoms_hommes + prenoms_femmes)
        nom = random.choice(noms_famille)
        phone = generer_numero_guineen()
        adresse = f"{random.choice(zones_conakry)}, Conakry"
        while User.objects.filter(phone=phone).exists():
            phone = generer_numero_guineen()
        repetiteur_user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': prenom,
                'last_name': nom,
                'role': 'repetiteur',
                'adresse': adresse,
                'is_validated': True,
            }
        )
        repetiteur_user.set_password('karamoko')
        repetiteur_user.save()
        repetiteur, created = Repetiteur.objects.get_or_create(
            user=repetiteur_user,
            defaults={
                'biographie': "Encadrant toutes matières du lycée.",
                'experience': random.randint(5, 20),
                'prix_par_seance': 300000,
                'disponibilite_matin': True,
                'disponibilite_apres_midi': True,
                'disponibilite_soir': True,
                'disponibilite_weekend': True,
                'is_soumis': True,
                'cgu_acceptees': True,
                'avatar': create_dummy_file(f"avatar_lycee_{i}.jpg", "Image avatar"),
                'piece_identite': create_dummy_file(f"carte_id_lycee_{i}.pdf", "Carte d'identité"),
                'diplome': create_dummy_file(f"diplome_lycee_{i}.pdf", "Diplôme universitaire"),
                'contrat_ecole': create_dummy_file(f"contrat_lycee_{i}.pdf", "Contrat école"),
            }
        )
        cours_selectionnes = [cours_objects[m] for m in matieres_lycee if m in cours_objects]
        repetiteur.cours.set(cours_selectionnes)
        repetiteurs.append(repetiteur_user)
        print(f"✅ Répétiteur LYCÉE créé: {repetiteur_user.first_name} {repetiteur_user.last_name} ({repetiteur_user.phone})")

    # 15 répétiteurs classiques
    for i in range(15):
        prenom = random.choice(prenoms_hommes + prenoms_femmes)
        nom = random.choice(noms_famille)
        phone = generer_numero_guineen()
        adresse = f"{random.choice(zones_conakry)}, Conakry"
        while User.objects.filter(phone=phone).exists():
            phone = generer_numero_guineen()
        repetiteur_user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': prenom,
                'last_name': nom,
                'role': 'repetiteur',
                'adresse': adresse,
                'is_validated': True,
            }
        )
        repetiteur_user.set_password('karamoko')
        repetiteur_user.save()
        repetiteur, created = Repetiteur.objects.get_or_create(
            user=repetiteur_user,
            defaults={
                'biographie': "Répétiteur généraliste.",
                'experience': random.randint(2, 20),
                'prix_par_seance': random.choice([150000, 200000, 250000, 300000]),
                'disponibilite_matin': random.choice([True, False]),
                'disponibilite_apres_midi': True,
                'disponibilite_soir': random.choice([True, False]),
                'disponibilite_weekend': random.choice([True, False]),
                'is_soumis': True,
                'cgu_acceptees': True,
                'avatar': create_dummy_file(f"avatar_{i}.jpg", "Image avatar"),
                'piece_identite': create_dummy_file(f"carte_id_{i}.pdf", "Carte d'identité"),
                'diplome': create_dummy_file(f"diplome_{i}.pdf", "Diplôme universitaire"),
                'contrat_ecole': create_dummy_file(f"contrat_{i}.pdf", "Contrat école"),
            }
        )
        cours_disponibles = list(cours_objects.values())
        nb_cours = random.randint(2, 5)
        cours_selectionnes = random.sample(cours_disponibles, nb_cours)
        repetiteur.cours.set(cours_selectionnes)
        repetiteurs.append(repetiteur_user)
        if created:
            print(f"✅ Répétiteur créé: {repetiteur_user.first_name} {repetiteur_user.last_name} ({repetiteur_user.phone})")

    # 8. CRÉER 20 DEMANDES DE SOUSCRIPTION
    from souscriptions.models import DemandeSouscription
    for i in range(20):
        souscripteur = random.choice(Souscripteur.objects.all())
        niveau = random.choice(list(niveaux.values()))
        matieres = random.sample(list(cours_objects.values()), random.randint(1, 3))
        offre_tarifaire = random.choice(list(OffreTarifaire.objects.all()))
        moyen_paiement = random.choice(list(MethodePaiement.objects.all()))
        creneaux = random.sample(['matin', 'apres_midi', 'soir', 'weekend'], random.randint(1, 3))
        demande = DemandeSouscription.objects.create(
            souscripteur=souscripteur,
            niveau=niveau,
            nombre_enfants=random.randint(1, 3),
            offre_tarifaire=offre_tarifaire,
            creneaux_preferes=creneaux,
            moyen_paiement=moyen_paiement,
            commentaire="Demande de test auto-générée.",
            statut='en_attente'
        )
        demande.matieres.set(matieres)
        print(f"✅ Demande de souscription créée pour {souscripteur}")

    # 9. CRÉER UN ADMINISTRATEUR
    admin_phone = "627116354"
    if not User.objects.filter(phone=admin_phone).exists():
        admin_user = User.objects.create_superuser(
            phone=admin_phone,
            first_name="Administrateur",
            last_name="Système",
            password="karamoko",
            adresse="Kaloum, Conakry",
        )
        admin_user.role = 'parent'  # ou créer un rôle admin si nécessaire
        admin_user.save()
        print(f"✅ Administrateur créé: {admin_user.phone}")
    
    print("\n🎉 Données de test créées avec succès!")
    print(f"📊 Résumé:")
    print(f"   - {Niveau.objects.count()} niveaux")
    print(f"   - {Cours.objects.count()} cours")
    print(f"   - {OffreTarifaire.objects.count()} offres tarifaires")
    print(f"   - {MethodePaiement.objects.count()} méthodes de paiement")
    print(f"   - {User.objects.filter(role='parent').count()} parents")
    print(f"   - {User.objects.filter(role='repetiteur').count()} répétiteurs")
    print(f"   - {Repetiteur.objects.count()} profils répétiteurs")
    print(f"   - {Souscripteur.objects.count()} profils souscripteurs")
    
    # Affichage des associations pour vérification
    print("\n🔍 Vérification des associations cours-niveaux:")
    for cours in Cours.objects.all():
        niveaux_associes = cours.niveaux.values_list('nom', flat=True)
        print(f"   - {cours.titre}: {', '.join(niveaux_associes)}")
    
    print("\n📱 Comptes créés:")
    print("   PARENTS/SOUSCRIPTEURS:")
    for parent in User.objects.filter(role='parent')[:5]:
        print(f"   - {parent.first_name} {parent.last_name}: {parent.phone}")
    
    print("   RÉPÉTITEURS:")
    for repetiteur in User.objects.filter(role='repetiteur')[:5]:
        print(f"   - {repetiteur.first_name} {repetiteur.last_name}: {repetiteur.phone}")
    
    print(f"\n   ADMIN: {admin_phone} (mot de passe: admin123)")
    print("   TOUS LES AUTRES: karamoko")


# Si c'est une commande de management
class Command(BaseCommand):
    help = 'Crée des données de test pour le système de souscription'
    
    def handle(self, *args, **options):
        create_test_data()

# Si vous l'exécutez directement dans le shell :
# python manage.py shell
# >>> exec(open('create_test_data.py').read())