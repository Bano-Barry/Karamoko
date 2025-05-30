from django.db import models
from authentication.models import CustomUser
from core.models import Niveau
from repetiteurs.models import Cours, Repetiteur
from paiements.models import MethodePaiement, OffreTarifaire, PlanTarifaire
from souscripteurs.models import Souscripteur

class DemandeSouscription(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('affectée', 'Affectée'),
        ('rejetée', 'Rejetée'),
    ]
    
    CRENEAU_CHOICES = [
        ('matin', 'Matin (8h-12h)'),
        ('apres_midi', 'Après-midi (14h-18h)'),
        ('soir', 'Soir (18h-20h)'),
        ('weekend', 'Weekend'),
    ]

    souscripteur = models.ForeignKey(Souscripteur, on_delete=models.CASCADE, related_name='demandes')
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True)
    matieres = models.ManyToManyField(Cours, related_name='demandes')
    nombre_enfants = models.PositiveIntegerField()
    offre_tarifaire = models.ForeignKey(OffreTarifaire, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Préférences de créneaux
    creneaux_preferes = models.JSONField(default=list, help_text="Liste des créneaux préférés")
    
    moyen_paiement = models.ForeignKey(MethodePaiement, on_delete=models.SET_NULL, null=True)
    commentaire = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    
    # Champs pour le suivi
    date_traitement = models.DateTimeField(null=True, blank=True)
    traite_par = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_traitees')

    def __str__(self):
        return f"Demande {self.souscripteur} ({self.niveau}) - {self.statut}"
    
    @property
    def cout_total_estime(self):
        """Calcule le coût total estimé selon l'offre choisie et le nombre d'enfants"""
        if self.offre_tarifaire:
            nombre_matieres = self.matieres.count()
            prix_base = self.offre_tarifaire.get_prix_pour_matieres(nombre_matieres)
            return prix_base * self.nombre_enfants
        return 0
    
class Souscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspendue', 'Suspendue'),
        ('expiree', 'Expirée'),
        ('annulee', 'Annulée'),
    ]
    
    souscripteur = models.ForeignKey(Souscripteur, on_delete=models.CASCADE, related_name="souscriptions")
    repetiteur = models.ForeignKey(Repetiteur, on_delete=models.CASCADE, related_name="souscriptions")
    cours = models.ManyToManyField(Cours, related_name="souscriptions")
    offre_tarifaire = models.ForeignKey(OffreTarifaire, on_delete=models.CASCADE, related_name="souscriptions")
    
    # Référence à la demande originale
    demande_origine = models.OneToOneField(DemandeSouscription, on_delete=models.SET_NULL, null=True, blank=True, related_name="souscription_creee")
    
    moyen_paiement = models.ForeignKey(MethodePaiement, on_delete=models.SET_NULL, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Suivi des séances
    seances_prevues = models.IntegerField(help_text="Nombre total de séances prévues")
    seances_effectuees = models.IntegerField(default=0, help_text="Nombre de séances effectuées")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    cree_par = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.souscripteur} → {self.repetiteur} ({self.offre_tarifaire}) du {self.date_debut} au {self.date_fin}"
    
    @property
    def progression(self):
        """Calcule le pourcentage de progression"""
        if self.seances_prevues > 0:
            return (self.seances_effectuees / self.seances_prevues) * 100
        return 0
    
    @property
    def seances_restantes(self):
        """Calcule le nombre de séances restantes"""
        return max(0, self.seances_prevues - self.seances_effectuees)
    
# Modèle représentant une séance effectuée dans le cadre d'une souscription
class PasserSeance(models.Model):
    souscription = models.ForeignKey(Souscription, on_delete=models.CASCADE, related_name="seances")  # Lien vers la souscription
    date = models.DateField()  # Date de la séance
    commentaire = models.TextField(blank=True, null=True)  # Commentaire optionnel sur la séance

    def __str__(self):
        # Représentation sous forme de chaîne de caractères de la séance
        return f"Seance {self.date} - {self.souscription}"

class Evaluation(models.Model):
    souscription = models.OneToOneField(Souscription, on_delete=models.CASCADE)
    note = models.IntegerField()  # 1 à 5 par exemple
    commentaire = models.TextField(blank=True, null=True)
