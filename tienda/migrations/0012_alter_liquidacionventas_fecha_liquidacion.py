# Generated by Django 5.1.1 on 2025-04-01 12:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0011_alter_libroventas_fecha_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liquidacionventas',
            name='fecha_liquidacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
