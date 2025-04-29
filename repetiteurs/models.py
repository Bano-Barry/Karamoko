from django.db import models
from authentication.models import CustomUser
from core.models import Niveau
from formations.models import Formation

class Competence(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Repetiteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name="repetiteur")
    avatar = models.ImageField(upload_to='avatars/repetiteurs/', blank=True, null=True)  
    biographie = models.TextField(blank=True, null=True)
    competences = models.ManyToManyField('repetiteurs.Competence', null=True, blank=True, related_name="repetiteurs")
    formations = models.ManyToManyField('formations.Formation', null=True, blank=True, related_name="repetiteurs")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"  # Combine le nom et le prénom


class Cours(models.Model):
    titre = models.CharField(max_length=200)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="cours")
    repetiteur = models.ForeignKey(Repetiteur, on_delete=models.CASCADE, related_name="cours")

    def __str__(self):
        return self.titre
