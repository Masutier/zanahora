from django.contrib import admin
from .models import Natural, Product


class NaturalAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'presenta', 'categoria', 'cantidad', 'costo', 'price', 'discount_price', 'perecedero')


admin.site.register(Natural, NaturalAdmin)
admin.site.register(Product, ProductAdmin)
