# Generated by Django 4.1 on 2023-10-05 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_remove_customer_imgid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='imgid',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images'),
        ),
    ]
