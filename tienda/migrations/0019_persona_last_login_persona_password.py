# Generated by Django 5.1.1 on 2025-04-12 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0018_remove_persona_password_persona_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$CTg8Dyft8y2tzvFxr8ZtUh$ta6z0QqQICoFEl6rgjFLY8UGoK1/5q+RBSFLZKvidZ4=', max_length=128),
        ),
    ]
