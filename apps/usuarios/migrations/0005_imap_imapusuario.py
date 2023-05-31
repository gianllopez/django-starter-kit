# Generated by Django 4.1.7 on 2023-05-26 03:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0004_usuario_foto"),
    ]

    operations = [
        migrations.CreateModel(
            name="IMAP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hostname", models.CharField(max_length=64)),
                ("puerto", models.IntegerField(default=993)),
            ],
        ),
        migrations.CreateModel(
            name="IMAPUsuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("servidor_usuario", models.CharField(max_length=255)),
                ("servidor_contrasena", models.TextField(max_length=128)),
                (
                    "servidor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="usuarios.imap"
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="IMAP",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
