from django.db import models
from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user', 'status']


class OrderFormStat(ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'complete', 'note', 'pay', 'pay_note', 'repartidor']
        exclude = ['user', 'customer', 'transaction_id']
