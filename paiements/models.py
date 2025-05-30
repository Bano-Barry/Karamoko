from django.db import models

from core.models import Niveau
from repetiteurs.models import Cours

class MethodePaiement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(default="Aucune description", blank=True,)

    def __str__(self):
        return self.nom

class OffreTarifaire(models.Model):
    """
    Modèle pour gérer les offres tarifaires selon le système éducatif guinéen
    """
    TYPE_OFFRE_CHOICES = [
        ('forfait_global', 'Forfait Global'),  # Primaire : toutes matières incluses
        ('par_matiere', 'Par Matière'),        # Collège/Lycée : facturation par matière
        ('pack_specialite', 'Pack Spécialité'), # Lycée 11-12ème : pack matières de spécialité
        ('pack_examen', 'Pack Examen'),        # 10ème : pack maths+physique+chimie
    ]
    
    nom = models.CharField(max_length=150, help_text="Ex: Primaire 1ère-5ème, Collège par matière")
    description = models.TextField(blank=True, null=True)
    type_offre = models.CharField(max_length=20, choices=TYPE_OFFRE_CHOICES)
    
    # Niveaux concernés par cette offre
    niveaux = models.ManyToManyField(Niveau, related_name="offres_tarifaires")
    
    # Prix et conditions
    prix_unitaire = models.IntegerField(help_text="Prix en GNF")  # Prix de base
    prix_combine = models.IntegerField(null=True, blank=True, help_text="Prix si plusieurs matières combinées")
    
    # Standard pour toutes les offres
    nombre_seances_mois = models.IntegerField(default=12, help_text="Nombre de séances par mois")
    duree_seance_max = models.IntegerField(default=180, help_text="Durée max d'une séance en minutes")
    jours_par_semaine = models.IntegerField(default=3, help_text="Nombre de jours par semaine")
    
    # Matières concernées (optionnel selon le type d'offre)
    matieres_incluses = models.ManyToManyField(Cours, blank=True, related_name="offres_tarifaires", help_text="Matières incluses dans l'offre")
    
    is_active = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")
    
    class Meta:
        ordering = ['ordre', 'prix_unitaire']
        verbose_name = "Offre Tarifaire"
        verbose_name_plural = "Offres Tarifaires"
    
    def __str__(self):
        return f"{self.nom} - {self.prix_unitaire:,} GNF"
    
    def get_prix_pour_matieres(self, nombre_matieres=1):
        """
        Calcule le prix selon le nombre de matières
        """
        if self.type_offre == 'forfait_global':
            return self.prix_unitaire  # Prix fixe quelque soit le nombre de matières
        
        elif self.type_offre == 'par_matiere':
            return self.prix_unitaire * nombre_matieres
        
        elif self.type_offre == 'pack_specialite':
            return self.prix_unitaire  # Prix fixe pour le pack
        
        elif self.type_offre == 'pack_examen' and nombre_matieres >= 3:
            # 10ème : si 3 matières combo, sinon prix unitaire
            return self.prix_combine or (self.prix_unitaire * nombre_matieres)
        
        return self.prix_unitaire * nombre_matieres
    
    def est_compatible_avec_niveau(self, niveau):
        """Vérifie si l'offre est compatible avec le niveau donné"""
        return self.niveaux.filter(id=niveau.id).exists()


class PlanTarifaire(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(default="Aucune description", blank=True,)
    duree = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class Paiement(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('reussi', 'Réussi'),
        ('echoue', 'Échoué'),
    ]
    souscription = models.ForeignKey('souscriptions.Souscription', on_delete=models.CASCADE, related_name="paiements")
    methode = models.ForeignKey(MethodePaiement, on_delete=models.CASCADE, related_name="paiements")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)

    def __str__(self):
        return f"{self.souscription} - {self.montant}"
