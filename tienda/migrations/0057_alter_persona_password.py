# Generated by Django 5.1.1 on 2025-05-09 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0056_alter_persona_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$EJXBmYMQZbVn2097SFqEZU$gBIL+v0oF8x1t6eGOBKX1tTWin0V8PfMSADZOAnu/Bs=', max_length=128),
        ),
    ]
