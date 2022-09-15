# Generated by Django 3.1.7 on 2021-02-28 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('mainAdmin', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('En Aprobación', 'En Aprobación'), ('Pago Realizado', 'Pago Realizado'), ('Pendiente', 'Pendiente'), ('En Ruta', 'En Ruta'), ('Entrega Confirmada', 'Entrega Confirmada'), ('Entregado', 'Entregado'), ('Rechazado', 'Rechazado')], default='En Aprobación', max_length=100, null=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('pay', models.CharField(blank=True, choices=[('Daviplata', 'Daviplata'), ('Nequi', 'Nequi'), ('Bitcoin', 'Bitcoin'), ('Contra Entrega', 'Contra Entrega')], max_length=50, null=True)),
                ('pay_note', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=80, null=True)),
                ('barrio', models.CharField(blank=True, max_length=80, null=True)),
                ('city', models.CharField(blank=True, default='Bogotá', max_length=80, null=True)),
                ('state', models.CharField(blank=True, default='Bogotá D.C.', max_length=80, null=True)),
                ('country', models.CharField(blank=True, default='Colombia', max_length=80, null=True)),
                ('zipcode', models.CharField(blank=True, default='111311', max_length=10, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modify', models.DateTimeField(auto_now=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.customer')),
                ('repartidor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainAdmin.repartidor')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('itemPrice', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('itemCosto', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
    ]
