# Generated by Django 5.1.1 on 2025-04-01 12:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0009_alter_compracorporativa_fecha_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_entrega',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
