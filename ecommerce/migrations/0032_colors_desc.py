# Generated by Django 4.1 on 2023-10-11 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0031_rename_gen_customer_gender_remove_colors_desc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='colors',
            name='desc',
            field=models.CharField(blank=True, default='color', max_length=25, null=True),
        ),
    ]