# Generated by Django 5.1.1 on 2025-03-27 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='rut',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
    ]
