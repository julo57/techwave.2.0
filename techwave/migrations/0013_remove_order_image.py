# Generated by Django 5.0.2 on 2024-02-25 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('techwave', '0012_order_image_order_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='image',
        ),
    ]
