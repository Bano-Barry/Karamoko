from django.db import models

class MethodePaiement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class PlanTarifaire(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class Paiement(models.Model):
    souscription = models.ForeignKey('souscriptions.Souscription', on_delete=models.CASCADE, related_name="paiements")
    methode = models.ForeignKey(MethodePaiement, on_delete=models.CASCADE, related_name="paiements")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.souscription} - {self.montant}"
