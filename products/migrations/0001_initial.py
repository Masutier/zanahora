# Generated by Django 3.1.7 on 2021-02-28 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Natural',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=15, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('icon', models.ImageField(default='media/img/icons/logosolo.png', upload_to='media/img/icons/natural')),
                ('descrip', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Apply', 'Apply'), ('Aproved', 'Aproved'), ('Void', 'Void'), ('Delete', 'Delete')], default='Apply', max_length=10, null=True)),
                ('categoria', models.CharField(blank=True, choices=[('Verduras', 'Verduras'), ('Legumbres', 'Legumbres'), ('Tuberculos', 'Tuberculos'), ('Frutas', 'Frutas'), ('Frutos_Secos', 'Frutos_Secos'), ('Aceites', 'Aceites'), ('Endulzantes', 'Endulzantes'), ('Especias', 'Especias'), ('Conservas', 'Conservas'), ('Bebidas', 'Bebidas'), ('Pasabocas', 'Pasabocas'), ('Proteina_Vegetal', 'Proteina_Vegetal'), ('Cosmetica', 'Cosmetica'), ('Otro', 'Otro')], max_length=30, null=True)),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('contenido', models.CharField(blank=True, choices=[('Gluten', 'gluten'), ('Lacteo', 'Lacteo'), ('Syrup', 'Syrup'), ('Soya', 'Soya'), ('Maní', 'Maní')], max_length=15, null=True)),
                ('foto1', models.ImageField(default='media/img/products/defaultProduct.png', upload_to='media/img/products')),
                ('foto2', models.ImageField(blank=True, null=True, upload_to='media/img/products')),
                ('foto3', models.ImageField(blank=True, null=True, upload_to='media/img/products')),
                ('foto4', models.ImageField(blank=True, null=True, upload_to='media/img/products')),
                ('description', models.TextField(blank=True, null=True)),
                ('presenta', models.CharField(blank=True, max_length=10, null=True)),
                ('cantidad', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('label', models.CharField(blank=True, choices=[('Usual', 'Usual'), ('Nuevo', 'Nuevo'), ('Oferta', 'Oferta'), ('Especial', 'Especial')], max_length=10, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('costo', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('perecedero', models.BooleanField(blank=True, default=True, null=True)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modify', models.DateTimeField(auto_now=True, null=True)),
                ('estilo', models.ManyToManyField(blank=True, to='users.Estilo')),
                ('natural', models.ManyToManyField(blank=True, to='products.Natural')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
