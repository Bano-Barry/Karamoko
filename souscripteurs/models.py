from django.db import models

from authentication.models import CustomUser

class Souscripteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name="souscripteur")
    avatar = models.ImageField(upload_to='avatars/souscripteurs/', blank=True, null=True) 
    cgu_acceptees = models.BooleanField(default=False)  # Acceptation des CGU
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"  # Combine le nom et le prénom
