# Generated by Django 5.1.1 on 2025-05-05 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0025_alter_persona_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$nt1rFMbK6gfF7hlrumvp5d$/SUlfwluQm8n1T+jQDEHipDNZ8ZQYYlQDmN+Pr8cCeI=', max_length=128),
        ),
    ]
