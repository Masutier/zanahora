from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    DOCUM = (
        ('CC', 'CC'),
        ('Passport', 'Passport'),
        ('Otro', 'Otro')
    )
    STATUS = (
        ('Apply', 'Apply'),
        ('Aproved', 'Aproved'),
        ('Void', 'Void'),
        ('Delete', 'Delete')
    )
    MODELO = (
        ('Agrícola', 'Agrícola'),
        ('Procesados', 'Procesados'),
        ('Artesanal', 'Artesanal'),
        ('Otro', 'Otro')
    )
    status = models.CharField(max_length=10, blank=True, null=True, default='Apply', choices=STATUS)
    modelo = models.CharField(max_length=10, blank=True, null=True, choices=MODELO)
    Convenio = models.TextField(blank=True, null=True)

    name = models.CharField(max_length=60, blank=True, null=True)
    nit = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=200,blank=True, null=True)
    phoneNum = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)

    represent = models.CharField(max_length=60, blank=True, null=True)
    reptydoc = models.CharField(max_length=10, blank=True, null=True, default='CC', choices=DOCUM)
    repcedulaId = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    contact = models.CharField(max_length=60, blank=True, null=True)
    contydoc = models.CharField(max_length=10, blank=True, null=True, default='CC', choices=DOCUM)
    concedulaId = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)

    projectDescr = models.TextField(blank=True, null=True)
    productDescr = models.TextField(blank=True, null=True)
    otherDescr = models.TextField(blank=True, null=True)

    address = models.CharField(max_length=80, blank=True, null=True)
    barrio = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True, default='Bogotá')
    state = models.CharField(max_length=80, blank=True, null=True, default='Bogotá D.C.')
    country = models.CharField(max_length=80, blank=True, null=True, default='Colombia')
    zipcode = models.CharField(max_length=6, blank=True, null=True, default='111311')

    logo = models.ImageField(default='media/img/projects/logosolo.png', upload_to='media/img/projects')
    foto1 = models.ImageField(default='media/img/projects/logosolo.png', upload_to='media/img/projects')
    foto2 = models.ImageField(upload_to='media/img/products', blank=True, null=True)
    foto3 = models.ImageField(upload_to='media/img/products', blank=True, null=True)
    foto4 = models.ImageField(upload_to='media/img/products', blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modify = models.DateTimeField(auto_now_add=False, auto_now = True, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("proj_detail", kwargs={"id": self.id})


class Video(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True, null=True)
    thumbnail = models.ImageField(default='media/img/videos/defaultVideo.png', upload_to='media/img/videos', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title
