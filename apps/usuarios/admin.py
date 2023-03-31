from django.contrib import admin
from django.contrib.auth import get_user_model

from .forms import UsuarioForm
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioForm
    list_display = [
        "usuario",
        "nombre",
        "apellido",
        "correo_electronico",
    ]

    def get_queryset(self, *args, **kwargs):
        return get_user_model().objects.filter(is_superuser=False)
