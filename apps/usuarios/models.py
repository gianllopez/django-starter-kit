from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UsuarioManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    usuario = models.CharField(max_length=12, unique=True)
    correo_electronico = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "usuario"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.usuario} / {self.correo_electronico}"
