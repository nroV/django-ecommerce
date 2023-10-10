# Generated by Django 4.1 on 2023-10-10 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0017_address_description_alter_address_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('colorselection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.colors')),
                ('imageproduct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images')),
            ],
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='method',
            field=models.CharField(blank=True, default='Cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='products',
            field=models.ManyToManyField(through='ecommerce.Order', to='ecommerce.product'),
        ),
        migrations.DeleteModel(
            name='OrderProduct',
        ),
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.orderdetail'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product'),
        ),
    ]
