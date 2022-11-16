from django.db import models
from django.contrib.auth.models import User
from django.db.models import ManyToManyField
from django.utils import timezone
from datetime import datetime


# Create your models here.
class Communaute(models.Model):
    nom = models.CharField(max_length=100)
    abonnes = models.ManyToManyField(User, verbose_name='abonnes')

    def recherche_abonnement(self, user):
        for abo in self.abonnes.all():
            if user.id == abo.id:
                return True
        return False

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

#J'ai du modifie Priorite en priorite, pour ne pas avoir d'erreur en appelant Priorite.object.get(label='Ecarlate')
#Dans une vue
class priorite(models.Model):
    label = models.CharField(max_length=100)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label

class Post(models.Model):
    titre = models.CharField(max_length=200, default='')
    description = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    priorite = models.ForeignKey(priorite, on_delete=models.CASCADE)
    evenementiel = models.BooleanField(null=True)
    date_evenement = models.DateTimeField(null=True, default=datetime.now())
    likes = models.ManyToManyField(User, null=True, verbose_name='likes', related_name='+')
    vues = models.ManyToManyField(User, null=True, verbose_name='vus', related_name='++')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.titre

    def recherche_auteur(self, user):
        if user.id == self.auteur:
            return True
        else:
            return False

    def recherche_like(self, user):
        for abo in self.likes.all():
            if user.id == abo.id:
                return True
        return False

    def recherche_vue(self, user):
        for abo in self.vues.all():
            if user.id == abo.id:
                return True
        return False

class Commentaire(models.Model):
    date_creation = models.DateTimeField(default=timezone.now)
    contenu = models.TextField(default='Super !')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return self.contenu

