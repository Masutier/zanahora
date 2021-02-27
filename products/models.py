from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from projects.models import Project
from users.models import Estilo


class Natural(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(default='media/img/icons/logosolo.png', upload_to='media/img/icons/natural')
    descrip = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    LABEL = (
        ('Usual', 'Usual'),
        ('Nuevo', 'Nuevo'),
        ('Oferta', 'Oferta'),
        ('Especial', 'Especial')
    )
    CONTENIDO = (
        ('Gluten', 'gluten'),
        ('Lacteo', 'Lacteo'),
        ('Syrup', 'Syrup'),
        ('Soya', 'Soya'),
        ('Maní', 'Maní'),
    )
    STATUS = (
        ('Apply', 'Apply'),
        ('Aproved', 'Aproved'),
        ('Void', 'Void'),
        ('Delete', 'Delete')
    )
    CATEGORY = (
        ('Verduras', 'Verduras'),
        ('Legumbres', 'Legumbres'),
        ('Tuberculos', 'Tuberculos'),
        ('Frutas', 'Frutas'),
        ('Frutos_Secos', 'Frutos_Secos'),
        ('Aceites', 'Aceites'),
        ('Endulzantes', 'Endulzantes'),
        ('Especias', 'Especias'),
        ('Conservas', 'Conservas'),
        ('Bebidas', 'Bebidas'),
        ('Pasabocas', 'Pasabocas'),
        ('Proteina_Vegetal', 'Proteina_Vegetal'),
        ('Cosmetica', 'Cosmetica'),
        ('Otro', 'Otro')
    )
    status = models.CharField(max_length=10, blank=True, null=True, default='Apply', choices=STATUS)
    categoria = models.CharField(max_length=30, blank=True, null=True, choices=CATEGORY)
    natural = models.ManyToManyField(Natural, blank=True)
    estilo = models.ManyToManyField(Estilo, blank=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    contenido = models.CharField(max_length=15, blank=True, null=True, choices=CONTENIDO)
    foto1 = models.ImageField(default='media/img/products/defaultProduct.png', upload_to='media/img/products')
    foto2 = models.ImageField(upload_to='media/img/products', blank=True, null=True)
    foto3 = models.ImageField(upload_to='media/img/products', blank=True, null=True)
    foto4 = models.ImageField(upload_to='media/img/products', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    presenta = models.CharField(max_length=10, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    label = models.CharField(max_length=10, blank = True, null=True, choices=LABEL)
    price = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    costo = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    perecedero = models.BooleanField(default=True, blank=True, null=True)
    digital = models.BooleanField(default=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modify = models.DateTimeField(auto_now_add=False, auto_now = True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("prod_detail", kwargs={"id": self.id})

    def get_add_to_costal_url(self):
        return reverse("add_to_costal", kwargs={"id": self.id})

