# backend/api/models.py

from django.db import models
from django.contrib.auth.models import User

# Enumerações para as escolhas (choices)
class GroupType(models.TextChoices):
    CORAL = 'Coral', 'Coral'
    ORQUESTRA = 'Orquestra', 'Orquestra'

class Naipe(models.TextChoices):
    TENOR = 'Tenor', 'Tenor'
    BAIXO = 'Baixo', 'Baixo'
    SOPRANO = 'Soprano', 'Soprano'
    CONTRALTO = 'Contralto', 'Contralto'

class OrquestraGrupo(models.TextChoices):
    NOVOS = 'Novos', 'Novos'
    GRUPO1 = 'Grupo 1', 'Grupo 1'
    GRUPO2 = 'Grupo 2', 'Grupo 2'
    GRUPO3 = 'Grupo 3', 'Grupo 3'
    GRUPO4 = 'Grupo 4', 'Grupo 4'

class UserRole(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    MAESTRO = 'Maestro', 'Maestro'

class RepertorioItem(models.Model):
    type = models.CharField(max_length=20, choices=GroupType.choices)
    title = models.CharField(max_length=200)
    arrangement = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField()
    audioUrl = models.URLField(max_length=500, blank=True, null=True)
    videoUrl = models.URLField(max_length=500, blank=True, null=True)
    sheetMusicUrl = models.URLField(max_length=500)
    naipes = models.JSONField(default=list, blank=True)
    grupos = models.JSONField(default=list, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class AgendaItem(models.Model):
    group = models.CharField(max_length=20, choices=GroupType.choices)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class RecadoItem(models.Model):
    group = models.CharField(max_length=20, choices=GroupType.choices)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class HistoriaItem(models.Model):
    year = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    imageUrl = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.year} - {self.title}"

class GaleriaItem(models.Model):
    type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    url = models.URLField(max_length=500)
    thumbnailUrl = models.URLField(max_length=500)
    title = models.CharField(max_length=200)
    group = models.CharField(max_length=20, choices=GroupType.choices)

    def __str__(self):
        return self.title

# O modelo User já vem com o Django, não precisamos de o redefinir,
# a menos que você queira um Perfil de Utilizador customizado, o que podemos fazer mais tarde.
