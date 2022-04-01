# Generated by Django 4.0.3 on 2022-03-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_cost_product_cost_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]