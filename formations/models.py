from django.db import models
from repetiteurs.models import Repetiteur

# Modèle représentant un type de formation
class TypeFormation(models.Model):
    nom = models.CharField(max_length=100)  # Nom du type de formation
    description = models.TextField(blank=True, null=True)  # Description du type de formation (facultatif)

    def __str__(self):
        return self.nom


# Modèle représentant une formation
class Formation(models.Model):
    titre = models.CharField(max_length=200)  # Titre de la formation
    type_formation = models.ForeignKey(
        TypeFormation, 
        on_delete=models.CASCADE, 
        related_name="formations"
    )  # Type de formation associé

    def __str__(self):
        return self.titre
