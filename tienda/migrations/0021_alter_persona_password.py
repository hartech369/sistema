# Generated by Django 5.1.1 on 2025-04-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0020_alter_persona_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$g9GAxgDfFtxnn3DovAwHQ5$kkxrFdUqnFzUpHmoCWQrrwxcf7QdCpeo+l/7ezBs2rM=', max_length=128),
        ),
    ]
