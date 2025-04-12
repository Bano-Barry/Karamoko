from django.db import models

class Repetiteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/repetiteurs/', blank=True, null=True)
    competences = models.ManyToManyField('core.Competence')  
    formations = models.ManyToManyField('core.TypeFormation')  

    def __str__(self):
        return self.nom
