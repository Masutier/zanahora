from django.urls import path, include
from .views import *

urlpatterns = [
    path('adminHome/', adminHome, name="adminHome"),
    
    # PRODUCTS
    path('products_categ/', productsCateg, name="products_categ"),
    path('products_project/', productsProject, name="products_project"),
    path('prod_invent/', inventoryProduct, name="prod_invent"),

    path('projects/', projects, name="projects"),

    path('ventas_detail', ventasDetail, name='ventas_all'),

    path('lista_pedidos/', listaPedidos, name="lista_pedidos"),

    # PDFs
    path('oc_reparto_PDF/<str:pk>/', ocRepartoPDF, name="oc_reparto_PDF"),
    path('oc_reparto_DownloadPDF/<str:pk>/', ocRepartoDownloadPDF, name="oc_reparto_DownloadPDF"),

    path('order_compra_PDF/', ordenCompraPDF, name="order_compra_PDF"),
    path('order_compra_DownloadPDF/', ordenCompraDownloadPDF, name="order_compra_DownloadPDF"),
]