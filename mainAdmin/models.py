from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from projects.models import Project


class Repartidor(models.Model):
    REPARTDOCUM = (
        ('CC', 'CC'),
        ('Passport', 'Passport'),
        ('Otro', 'Otro')
    )
    name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=200,blank=True, null=True)
    foto = models.ImageField(default='media/img/repartidor/defaultUser.png', upload_to='media/img/repartidor')
    tydoc = models.CharField(max_length=10, blank=True, null=True, default='CC', choices=REPARTDOCUM)
    cedulaId = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    phoneNum = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modify = models.DateTimeField(auto_now_add=False, auto_now = True, blank=True, null=True)

    def __str__(self):
        return self.name
