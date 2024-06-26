# Generated by Django 5.0.3 on 2024-03-23 02:06

import datetime
import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=25)),
                ('code', models.CharField(blank=True, default='#EEEEEE', max_length=10, null=True)),
                ('price', models.FloatField(default=0)),
                ('stockqty', models.IntegerField(default=0)),
                ('desc', models.CharField(blank=True, default='color', max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=25)),
                ('lastname', models.CharField(max_length=25)),
                ('username', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('isowner', models.BooleanField(default=False, null=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_activated', models.BooleanField(default=False)),
                ('gender', models.CharField(blank=True, default='Other', max_length=25)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2024, 3, 23, 9, 6, 47, 864056))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(default=None, error_messages='image cannot be empty', upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, default='kg', max_length=25, null=True)),
                ('brand', models.CharField(blank=True, max_length=25, null=True)),
                ('model', models.CharField(blank=True, max_length=25, null=True)),
                ('material_name', models.CharField(blank=True, max_length=100, null=True)),
                ('colorid', models.ManyToManyField(blank=True, to='ecommerce.colors')),
                ('size', models.ManyToManyField(blank=True, to='ecommerce.sizes')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=55)),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=20, null=True)),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=20, null=True)),
                ('description', models.CharField(default='Current Location', max_length=255)),
                ('country', models.CharField(blank=True, default='Cambodia', max_length=255, null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to='ecommerce.customer')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='imgid',
            field=models.ForeignKey(blank=True, default=29, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.images'),
        ),
        migrations.AddField(
            model_name='colors',
            name='imgid',
            field=models.OneToOneField(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(error_messages='category cannot be empty', max_length=25)),
                ('imgid', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, max_length=125, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='ecommerce.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivered', models.BooleanField(default=False)),
                ('shipped_at', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('method', models.CharField(blank=True, default='Cash', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ispaid', models.BooleanField(default=False)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=0, editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(error_messages='product cannot be empty', max_length=45)),
                ('price', models.FloatField(default=0)),
                ('stockqty', models.IntegerField(default=0)),
                ('avg_rating', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('discount', models.IntegerField(default=0, null=True)),
                ('sell_rating', models.IntegerField(default=0, null=True)),
                ('description', models.CharField(default='This is a product description', max_length=100)),
                ('attribution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='ecommerce.attributes')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='ecommerce.category')),
                ('imgid', models.ManyToManyField(to='ecommerce.images')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('colorselection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.colors')),
                ('imageproduct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.orderdetail')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.sizes')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='products',
            field=models.ManyToManyField(through='ecommerce.OrderProduct', to='ecommerce.product'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer')),
                ('products', models.ManyToManyField(blank=True, to='ecommerce.product')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product')),
            ],
        ),
        migrations.CreateModel(
            name='SuperDeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dealname', models.CharField(blank=True, max_length=25, null=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imgid', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images')),
                ('product', models.ManyToManyField(to='ecommerce.product')),
            ],
        ),
    ]
