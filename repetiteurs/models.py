from django.db import models
from authentication.models import CustomUser
from core.models import Niveau
from formations.models import Formation

class Competence(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Cours(models.Model):
    titre = models.CharField(max_length=255, unique=True)  # Titre unique pour éviter les doublons
    description = models.TextField(blank=True, null=True)  # Description optionnelle

    def __str__(self):
        return self.titre

class Repetiteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="repetiteur")
    avatar = models.ImageField(upload_to='avatars/repetiteurs/', )
    biographie = models.TextField()
    competences = models.ManyToManyField('repetiteurs.Competence', related_name="repetiteurs")
    # formations = models.ManyToManyField('repetiteurs.Formation', blank=True, related_name="repetiteurs")
    cours = models.ManyToManyField('repetiteurs.Cours', related_name="repetiteurs")
    piece_identite = models.FileField(upload_to="documents/pieces_id/", )
    diplome = models.FileField(upload_to="documents/diplomes/", )
    contrat_ecole = models.FileField(upload_to="documents/contrats/", )
    # annees d'experience
    experience = models.IntegerField(null=True, blank=True)  # Nombre d'années d'expérience
    prix_par_seance = models.IntegerField(null=True, blank=True)  # Prix par séance en FCFA
    # zone = models.CharField(max_length=100, )
    date_soumission = models.DateTimeField(auto_now_add=True)
    is_soumis = models.BooleanField(default=False)
    cgu_acceptees = models.BooleanField(default=False)  # Acceptation des CGU 

    def is_profile_complete(self):
        """Vérifie que tous les champs obligatoires sont remplis"""
        return all([
            self.avatar,
            self.biographie,
            self.competences.exists(),
            self.cours.exists(),
            self.diplome,
            self.piece_identite,
            # self.zone,
            self.experience is not None,
            self.contrat_ecole,
            self.prix_par_seance is not None,
        ])

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"  # Combine le nom et le prénom


