from django.contrib import admin
from .models import Estilo, Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phoneNum', 'date_created')


admin.site.register(Estilo)
admin.site.register(Customer, CustomerAdmin)
