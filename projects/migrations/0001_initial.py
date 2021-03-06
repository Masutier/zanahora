# Generated by Django 3.1.7 on 2021-02-28 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Apply', 'Apply'), ('Aproved', 'Aproved'), ('Void', 'Void'), ('Delete', 'Delete')], default='Apply', max_length=10, null=True)),
                ('modelo', models.CharField(blank=True, choices=[('Agrícola', 'Agrícola'), ('Procesados', 'Procesados'), ('Artesanal', 'Artesanal'), ('Otro', 'Otro')], max_length=10, null=True)),
                ('Convenio', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('nit', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('phoneNum', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('represent', models.CharField(blank=True, max_length=60, null=True)),
                ('reptydoc', models.CharField(blank=True, choices=[('CC', 'CC'), ('Passport', 'Passport'), ('Otro', 'Otro')], default='CC', max_length=10, null=True)),
                ('repcedulaId', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True)),
                ('contact', models.CharField(blank=True, max_length=60, null=True)),
                ('contydoc', models.CharField(blank=True, choices=[('CC', 'CC'), ('Passport', 'Passport'), ('Otro', 'Otro')], default='CC', max_length=10, null=True)),
                ('concedulaId', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True)),
                ('projectDescr', models.TextField(blank=True, null=True)),
                ('productDescr', models.TextField(blank=True, null=True)),
                ('otherDescr', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=80, null=True)),
                ('barrio', models.CharField(blank=True, max_length=80, null=True)),
                ('city', models.CharField(blank=True, default='Bogotá', max_length=80, null=True)),
                ('state', models.CharField(blank=True, default='Bogotá D.C.', max_length=80, null=True)),
                ('country', models.CharField(blank=True, default='Colombia', max_length=80, null=True)),
                ('zipcode', models.CharField(blank=True, default='111311', max_length=6, null=True)),
                ('logo', models.ImageField(default='media/img/projects/logosolo.png', upload_to='media/img/projects')),
                ('foto1', models.ImageField(default='media/img/projects/logosolo.png', upload_to='media/img/projects')),
                ('foto2', models.ImageField(blank=True, null=True, upload_to='media/img/products')),
                ('foto3', models.ImageField(blank=True, null=True, upload_to='media/img/products')),
                ('foto4', models.ImageField(blank=True, null=True, upload_to='media/img/products')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modify', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('video_url', models.CharField(blank=True, max_length=500, null=True)),
                ('thumbnail', models.ImageField(blank=True, default='media/img/videos/defaultVideo.png', null=True, upload_to='media/img/videos')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
