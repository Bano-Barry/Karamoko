from django.db import models
from core.models import Niveau

class Competence(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Repetiteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/repetiteurs/', blank=True, null=True)
    competences = models.ManyToManyField('repetiteurs.Competence', related_name="repetiteurs")

    def __str__(self):
        return self.nom


class Cours(models.Model):
    titre = models.CharField(max_length=200)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="cours")
    repetiteur = models.ForeignKey(Repetiteur, on_delete=models.CASCADE, related_name="cours")

    def __str__(self):
        return self.titre
