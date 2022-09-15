from django.urls import path, include
from .views import *


urlpatterns = [
    path('validate_cupon', validate_cupon, name="validate_cupon"),
    path('Cupones', Cupones, name="Cupones"),
    path('createCupon', createCupon, name="createCupon"),
]
