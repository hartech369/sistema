# Generated by Django 5.1.1 on 2025-04-01 12:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0013_alter_liquidaciondistribucion_fecha_liquidacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fechaEmision',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
