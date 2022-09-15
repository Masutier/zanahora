from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Coupon


class CreateCouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'

