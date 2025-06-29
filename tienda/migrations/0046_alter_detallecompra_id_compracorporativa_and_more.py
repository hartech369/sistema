# Generated by Django 5.1.1 on 2025-05-08 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0045_alter_persona_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecompra',
            name='id_compraCorporativa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.compracorporativa'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$6ebAP1K8OfBTuR7uTaCbzn$N6wlPKe4RLy2IHurZQZJs0sVyrZ3iAu88PJp85q5xLs=', max_length=128),
        ),
    ]
