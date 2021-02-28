from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name="home"),

    # INFORMACION
    path('info_agroecol', agroecologia, name="info_agroecol"),
    path('info_icons', informacionIconos, name="info_icons"),
    path('info_entregas', infoEntregas, name="info_entregas"),

    #path('info_us', informacionNosotros, name="info_us"),
    path('info_conditions', informacionConditions, name="info_conditions"),
    path('info_privacy', informacionPrivacy, name="info_privacy"),

]
