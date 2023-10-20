# Generated by Django 4.1 on 2023-10-10 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0019_rename_order_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='colors',
            name='imgid',
            field=models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='attributes',
            name='size',
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=25, null=True)),
                ('imgid', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.images')),
            ],
        ),
        migrations.AddField(
            model_name='attributes',
            name='size',
            field=models.ManyToManyField(blank=True, null=True, to='ecommerce.sizes'),
        ),
    ]