from django.urls import path, include
from .views import *


urlpatterns = [
    path('orders/', orders, name="orders"),
    path('orders_simple/', simpleOrders, name="orders_simple"),
    path('orders_detail_to_aprove/', ordersDetailToAprove, name="orders_detail_to_aprove"),
    path('orders_detail_confirm/', ordersDetailConfirm, name="orders_detail_confirm"),
    path('orders_detail_pending/', ordersDetailPending, name="orders_detail_pending"),
    path('orders_detail_ruta/', ordersDetailRuta, name="orders_detail_ruta"),
    path('orders_detail_deliv_conf/', ordersDetailDelivConfRuta, name="orders_detail_deliv_conf"),
    path('orders_detail_entregado/', ordersDetailDelivered, name="orders_detail_entregado"),
    path('orders_detail_reject/', ordersDetailReject, name="orders_detail_reject"),
    path('orders_deep/', ordersDeepSearch, name="orders_deep"),

]