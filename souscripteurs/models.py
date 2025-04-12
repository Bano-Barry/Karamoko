from django.db import models

class Souscripteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/souscripteurs/', blank=True, null=True)

    def __str__(self):
        return self.nom
