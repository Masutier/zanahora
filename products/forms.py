from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Product


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

