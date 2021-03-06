# Generated by Django 3.1.7 on 2021-02-28 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estilo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=15, null=True)),
                ('icon', models.ImageField(default='media/img/icons/logosolo.png', upload_to='media/img/icons/estilo')),
                ('descrip', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(default='media/img/profile_pics/defaultUser.png', upload_to='media/img/profile_pics')),
                ('tydoc', models.CharField(blank=True, choices=[('CC', 'CC'), ('Passport', 'Passport'), ('Otro', 'Otro')], default='CC', max_length=10, null=True)),
                ('cedulaId', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True)),
                ('phoneNum', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('notasuser', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=80, null=True)),
                ('barrio', models.CharField(blank=True, max_length=80, null=True)),
                ('city', models.CharField(blank=True, default='Bogotá', max_length=80, null=True)),
                ('state', models.CharField(blank=True, default='Bogotá D.C.', max_length=80, null=True)),
                ('country', models.CharField(blank=True, default='Colombia', max_length=80, null=True)),
                ('zipcode', models.CharField(blank=True, default='111311', max_length=6, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('estilo', models.ManyToManyField(blank=True, to='users.Estilo')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
