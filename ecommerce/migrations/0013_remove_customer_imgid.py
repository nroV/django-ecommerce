# Generated by Django 4.1 on 2023-10-05 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_rename_created_at_orderdetail_shipped_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='imgid',
        ),
    ]