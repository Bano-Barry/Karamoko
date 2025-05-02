from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('repetiteur', 'Répétiteur'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    phone = models.CharField(max_length=30, unique=True)
    adresse = models.CharField(max_length=100, default='Conakry')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
