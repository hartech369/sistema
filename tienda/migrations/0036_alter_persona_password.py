# Generated by Django 5.1.1 on 2025-05-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0035_remove_pedido_id_mix_carga_factura_idmixcarga_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$ztlie1AP8pxdK73AIEXD7J$mDo38GU1Xz8aKl4HK0S6AlXvfZD9FRTLQwLsn3a7fdI=', max_length=128),
        ),
    ]
