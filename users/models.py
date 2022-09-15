from django.db import models
from django.contrib.auth.models import User


class Estilo(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)
    icon = models.ImageField(default='media/img/icons/logosolo.png', upload_to='media/img/icons/estilo')
    descrip = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    DOCUM = (
        ('CC', 'CC'),
        ('Passport', 'Passport'),
        ('Otro', 'Otro')
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=200,blank=True, null=True)
    image = models.ImageField(default='media/img/profile_pics/defaultUser.png', upload_to='media/img/profile_pics')
    tydoc = models.CharField(max_length=10, blank=True, null=True, default='CC', choices=DOCUM)
    cedulaId = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    phoneNum = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    estilo = models.ManyToManyField(Estilo, blank=True)
    notasuser = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=80, blank=True, null=True)
    barrio = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True, default='Bogotá')
    state = models.CharField(max_length=80, blank=True, null=True, default='Bogotá D.C.')
    country = models.CharField(max_length=80, blank=True, null=True, default='Colombia')
    zipcode = models.CharField(max_length=6, blank=True, null=True, default='111311')
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

