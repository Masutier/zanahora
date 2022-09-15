from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from cupons.models import Coupon
from users.models import *
from mainAdmin.models import Repartidor
from products.models import Product


class Order(models.Model):
    STATUS = (
        ('En Aprobación', 'En Aprobación'),
        ('Pago Realizado', 'Pago Realizado'),
        ('Pendiente', 'Pendiente'),
        ('En Ruta', 'En Ruta'),
        ('Entrega Confirmada', 'Entrega Confirmada'),
        ('Entregado', 'Entregado'),
        ('Rechazado', 'Rechazado'),
    )
    PAYMENT = (
        ('Daviplata', 'Daviplata'),
        ('Nequi', 'Nequi'),
        ('Bitcoin', 'Bitcoin'),
        ('Contra Entrega', 'Contra Entrega'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, default='En Aprobación', choices=STATUS)
    complete = models.BooleanField(default=False, blank=False, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    pay = models.CharField(max_length=50, blank=True, null=True, choices=PAYMENT)
    pay_note = models.TextField(blank=True, null=True)
    repartidor = models.ForeignKey(Repartidor, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=80, blank=True, null=True)
    barrio = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True, default='Bogotá')
    state = models.CharField(max_length=80, blank=True, null=True, default='Bogotá D.C.')
    country = models.CharField(max_length=80, blank=True, null=True, default='Colombia')
    zipcode = models.CharField(max_length=10, blank=True, null=True, default='111311')
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modify = models.DateTimeField(auto_now_add=False, auto_now = True, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def perec(self):
        perec = 0
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.perecedero == True:
                perec += i.quantity
        return perec

    # Subtotals
    @property
    def get_cost_subtotal(self):
        orderitems = self.orderitem_set.all()
        subtotal = sum([item.hist_cost_total for item in orderitems])
        return subtotal

    @property
    def get_cart_subtotal(self):
        orderitems = self.orderitem_set.all()
        subtotal = sum([item.get_total for item in orderitems])
        return subtotal

    @property
    def hist_order_subtotal(self):
        orderitems = self.orderitem_set.all()
        subtotal = sum([item.hist_get_total for item in orderitems])
        return subtotal

    # Totals
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        total += 7000
        return total

    @property
    def hist_order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.hist_get_total for item in orderitems])
        total += 7000
        return total

    # Items in order
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True,)
    itemPrice = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    itemCosto = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def get_total(self):
        if self.product.discount_price:
            total = int(self.product.discount_price) * int(self.quantity)
        else:
            total = int(self.product.price) * int(self.quantity)
        return total

    @property
    def hist_get_total(self):
        total = int(self.itemPrice) * int(self.quantity)
        return total

    @property
    def hist_cost_total(self):
        total = int(self.itemCosto) * int(self.quantity)
        return total

