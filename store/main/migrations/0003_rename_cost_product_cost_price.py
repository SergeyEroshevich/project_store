# Generated by Django 4.0.3 on 2022-03-25 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_product_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cost',
            new_name='cost_price',
        ),
    ]