# Generated by Django 5.1.1 on 2025-04-12 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0017_persona_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='password',
        ),
        migrations.AddField(
            model_name='persona',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
