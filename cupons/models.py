from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modify = models.DateTimeField(auto_now_add=False, auto_now = True, blank=True, null=True)

    def __str__(self):
        return self.code
