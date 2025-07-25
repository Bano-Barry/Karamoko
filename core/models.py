from django.db import models

class Niveau(models.Model):
    nom = models.CharField(max_length=100)
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage (0=plus bas niveau)")
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return self.nom
    
class CGU(models.Model):
    version = models.CharField(max_length=10, default="1.0")
    texte = models.TextField()
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CGU v{self.version} ({self.date_mise_a_jour.date()})"