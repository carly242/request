import datetime
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class CustomUser(AbstractUser):
    numero = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', default='photos/default.png')

    def __str__(self):
        return self.username


# models.py

from django.conf import settings

class OffreColis(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poids_disponible = models.FloatField(default='0')
    date_voyage = models.DateField(default=datetime.date.today)
    ville_depart = models.CharField(max_length=100)
    ville_destination = models.CharField(max_length=100, default='None')
    date_limite_contact = models.DateField(default=datetime.date.today)
    numero_contact = models.CharField(max_length=20, null=True)  # Champ pour le numéro de contact

    def __str__(self):
        return f"Offre de {self.utilisateur.username} - {self.poids_disponible} kg"



class Demande(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    numero_contact = models.CharField(max_length=20, null=True)  # Champ pour le numéro de contact

    def __str__(self):
        return f"Demande de {self.utilisateur.username} - {self.created_at}"
