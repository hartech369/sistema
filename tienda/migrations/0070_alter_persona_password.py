# Generated by Django 5.1.1 on 2025-05-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0069_alter_persona_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$r0Na76HZMryUXWixX9mSUq$XL+FdO71OTYQskbJbRwMl8YE6TAdpsGiMtf25/buGzc=', max_length=128),
        ),
    ]
