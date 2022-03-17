# Generated by Django 4.0.3 on 2022-03-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.BooleanField(choices=[('processing', 'Принято в обработку'), ('shipped', 'Упакован и отправлен'), ('delivered', 'Доставлен покупателю'), ('waiting', 'Ожидание поступления товара'), ('cancel', 'Отменен')], default='processing', verbose_name='Статус заказа'),
        ),
    ]
