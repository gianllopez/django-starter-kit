from os import path

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UsuarioManager


def get_upload_path_foto(instance, filename):
    return path.join(instance.usuario, filename)


class Usuario(AbstractBaseUser, PermissionsMixin):
    foto = models.ImageField(blank=True, null=True)
    nombre = models.CharField(max_length=255)
    usuario = models.CharField(max_length=12, unique=True)
    correo_electronico = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "usuario"

    def __str__(self):
        return self.usuario


class IMAP(models.Model):
    hostname = models.CharField(max_length=64)
    puerto = models.IntegerField(default=993)

    class Meta:
        verbose_name_plural = "IMAP"

    def __str__(self):
        return f"{self.hostname}:{self.puerto}"


class UsuarioIMAP(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="IMAP")
    servidor = models.ForeignKey(IMAP, on_delete=models.CASCADE)
    servidor_usuario = models.CharField(max_length=255)
    servidor_contrasena = models.CharField(max_length=128)
    activo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "IMAP de usuario"

    def __str__(self):
        return f"{self.usuario} / {self.servidor}"
