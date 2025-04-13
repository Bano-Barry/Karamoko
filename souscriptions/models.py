from django.db import models
from repetiteurs.models import Repetiteur
from paiements.models import PlanTarifaire
from souscripteurs.models import Souscripteur

# Modèle représentant une souscription entre un souscripteur et un répétiteur
class Souscription(models.Model):
    souscripteur = models.ForeignKey(Souscripteur, on_delete=models.CASCADE, related_name="souscriptions")  # Lien vers le souscripteur
    repetiteur = models.ForeignKey(Repetiteur, on_delete=models.CASCADE, related_name="souscriptions")  # Lien vers le répétiteur
    plan_tarifaire = models.ForeignKey(PlanTarifaire, on_delete=models.CASCADE, related_name="souscriptions")  # Lien vers le plan tarifaire
    date_debut = models.DateField()  # Date de début de la souscription
    date_fin = models.DateField()  # Date de fin de la souscription

    def __str__(self):
        # Représentation sous forme de chaîne de caractères de la souscription
        return f"{self.souscripteur} -> {self.repetiteur}"


# Modèle représentant une séance effectuée dans le cadre d'une souscription
class PasserSeance(models.Model):
    souscription = models.ForeignKey(Souscription, on_delete=models.CASCADE, related_name="seances")  # Lien vers la souscription
    date = models.DateField()  # Date de la séance
    commentaire = models.TextField(blank=True, null=True)  # Commentaire optionnel sur la séance

    def __str__(self):
        # Représentation sous forme de chaîne de caractères de la séance
        return f"Seance {self.date} - {self.souscription}"
