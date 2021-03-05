from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('prod_all/', csrf_exempt(prodAll), name='prod_all'),
    path('prod_by_category/<str:obj>', prod_by_category, name='prod_by_category'),
    path('prod_detail/<int:id>', product_detail, name='prod_detail'),
    path('prod_offert/', product_offert, name='prod_offert'),
    path('prod_special/', product_special, name='prod_special'),

# LOGS
    path('create_product/', createProduct, name="create_product"),
    path('update_product/<str:pk>', updateProduct, name="update_product"),
    path('fast_update_prod/<str:pk>', fastUpdateProduct, name="fast_update_prod"),
    path('delete_product/<str:pk>', deleteProduct, name="delete_product"),

]
