# Generated by Django 5.1.1 on 2025-05-08 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0049_alter_persona_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$T8Fe1u1w24Q2a5zDB8k8UH$5JxgxjTBm0y/X7yLBJi43FkxrUXPBVvn8G7ZSj5QH84=', max_length=128),
        ),
    ]
