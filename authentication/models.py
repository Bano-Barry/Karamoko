from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
# import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None, **extra_fields):
        if not phone:
            raise ValueError("Le numéro de téléphone est requis")
        if not first_name:
            raise ValueError("Le prénom est requis")
        if not last_name:
            raise ValueError("Le nom est requis")

        user = self.model(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.is_active = True  
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Un superuser doit avoir is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Un superuser doit avoir is_superuser=True.')

        return self.create_user(phone, first_name, last_name, password, **extra_fields)


# ==== USER MODEL ====

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('repetiteur', 'Répétiteur'),
    ]

    # uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=15, unique=True, verbose_name="Numéro de téléphone")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    adresse = models.CharField(max_length=100, default='Matam')
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)  # Pour savoir si l'utilisateur a validé son compte

    # Pas besoin de username ni email ici
    username = None
    email = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
