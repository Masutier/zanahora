from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),


# PRODUCTS
    path('products_categ/', productsCateg, name="products_categ"),
    path('products_project/', productsProject, name="products_project"),
    path('prod_invent/', inventoryProduct, name="prod_invent"),



]