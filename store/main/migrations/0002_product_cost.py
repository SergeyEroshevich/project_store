# Generated by Django 4.0.3 on 2022-03-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.FloatField(default=0),
        ),
    ]
