# Generated by Django 5.1.1 on 2025-06-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0088_alter_persona_password_alter_persona_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensajeContacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mensaje', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$zvliGpsqAgGSYkKK9Hxn5s$ZEiNqgQA0K/F6TscMhYOYzbumQJZ+CDLYlpmaWcdjAc=', max_length=128),
        ),
    ]
