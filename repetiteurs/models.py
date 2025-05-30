from django.db import models
from authentication.models import CustomUser
from core.models import Niveau
from formations.models import Formation

class Competence(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Cours(models.Model):
    titre = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    # Relation avec les niveaux - un cours peut être enseigné à plusieurs niveaux
    niveaux = models.ManyToManyField(Niveau, related_name="cours", help_text="Niveaux pour lesquels ce cours est disponible")
    
    def __str__(self):
        return self.titre

class Repetiteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="repetiteur")
    avatar = models.ImageField(upload_to='avatars/repetiteurs/')
    biographie = models.TextField()
    competences = models.ManyToManyField('repetiteurs.Competence', related_name="repetiteurs")
    cours = models.ManyToManyField('repetiteurs.Cours', related_name="repetiteurs")
    # Niveaux que le répétiteur peut enseigner
    niveaux = models.ManyToManyField(Niveau, related_name="repetiteurs", help_text="Niveaux que ce répétiteur peut enseigner")
    piece_identite = models.FileField(upload_to="documents/pieces_id/")
    diplome = models.FileField(upload_to="documents/diplomes/")
    contrat_ecole = models.FileField(upload_to="documents/contrats/")
    experience = models.IntegerField(null=True, blank=True)
    prix_par_seance = models.IntegerField(null=True, blank=True)
    # Disponibilités
    disponibilite_matin = models.BooleanField(default=False)
    disponibilite_apres_midi = models.BooleanField(default=False)
    disponibilite_soir = models.BooleanField(default=False)
    disponibilite_weekend = models.BooleanField(default=False)
    
    date_soumission = models.DateTimeField(auto_now_add=True)
    is_soumis = models.BooleanField(default=False)
    cgu_acceptees = models.BooleanField(default=False)

    def is_profile_complete(self):
        """Vérifie que tous les champs obligatoires sont remplis"""
        return all([
            self.avatar,
            self.biographie,
            self.competences.exists(),
            self.cours.exists(),
            self.niveaux.exists(),
            self.diplome,
            self.piece_identite,
            self.experience is not None,
            self.contrat_ecole,
            self.prix_par_seance is not None,
        ])

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

class ContratRepetiteur(models.Model):
    repetiteur = models.OneToOneField('Repetiteur', on_delete=models.CASCADE, related_name='contrat')
    fichier_pdf = models.FileField(upload_to='contrats_repetiteurs/', blank=True, null=True)
    date_generation = models.DateTimeField(auto_now_add=True)
    date_signature = models.DateTimeField(blank=True, null=True)
    accepte = models.BooleanField(default=False)
    version = models.CharField(max_length=10, default="1.0")

    def __str__(self):
        return f"Contrat {self.repetiteur.user.last_name} {self.repetiteur.user.first_name} (v{self.version})"