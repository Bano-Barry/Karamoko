from django.db import models

class TypeFormation(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Competence(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Niveau(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Repetiteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, blank=True, null=True)  # Nouveau champ pour le téléphone
    avatar = models.ImageField(upload_to='avatars/repetiteurs/', blank=True, null=True)  # Nouveau champ pour l'avatar
    competences = models.ManyToManyField(Competence)
    formations = models.ManyToManyField(TypeFormation)

    def __str__(self):
        return self.nom


class Cours(models.Model):
    titre = models.CharField(max_length=200)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    repetiteur = models.ForeignKey(Repetiteur, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


class Souscripteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, blank=True, null=True)  # Nouveau champ pour le téléphone
    avatar = models.ImageField(upload_to='avatars/souscripteurs/', blank=True, null=True)  # Nouveau champ pour l'avatar

    def __str__(self):
        return self.nom


class PlanTarifaire(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class Souscription(models.Model):
    souscripteur = models.ForeignKey(Souscripteur, on_delete=models.CASCADE)
    repetiteur = models.ForeignKey(Repetiteur, on_delete=models.CASCADE)
    plan_tarifaire = models.ForeignKey(PlanTarifaire, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"{self.souscripteur} -> {self.repetiteur}"


class MethodePaiement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Paiement(models.Model):
    souscription = models.ForeignKey(Souscription, on_delete=models.CASCADE)
    methode = models.ForeignKey(MethodePaiement, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.souscription} - {self.montant}"