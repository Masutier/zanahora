from django.urls import path, include
from .views import *


urlpatterns = [
    # CART 
    path('cart/', cart, name="cart"),
    path('checkout/<order_id>', checkout, name="checkout"),
    path('get_checkout_items/<order_id>', get_checkout_items, name="get_checkout_items"),
    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
    
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

    path('orders/order_detail/<str:pk>/', orderDetail, name="order_detail"),
    path('orders/pay_confirm/<str:pk>/', confirmaPago, name="pay_confirm"),
    path('orders/delivery_confirm/<str:pk>/', confirmaEntrega, name="delivery_confirm"),
    path('orders/update_order/<str:pk>/', updateOrder, name="update_order"),
    path('orders/update_order_stat/<str:pk>/', updateOrderStat, name="update_order_stat"),
    path('orders/delete_order/<str:pk>/', deleteOrder, name="delete_order"),
    path('orders/user_del_ord/<str:pk>/', userDelOrd, name="user_del_ord"),
]