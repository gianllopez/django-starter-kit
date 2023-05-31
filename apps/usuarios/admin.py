from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import ActualizarUsuarioForm, CrearUsuarioForm, GrupoForm
from .models import IMAP, Usuario, UsuarioIMAP

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GrupoForm


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    form = ActualizarUsuarioForm
    add_form = CrearUsuarioForm
    list_display = ["nombre", "usuario", "correo_electronico", "is_active"]
    list_filter = []
    fieldsets = [
        (
            "Información personal",
            {
                "fields": [
                    "foto",
                    "nombre",
                    "correo_electronico",
                ],
            },
        ),
        (
            "Credenciales",
            {
                "fields": [
                    "usuario",
                    "password",
                ]
            },
        ),
        (
            "Permisos",
            {"fields": ["groups"]},
        ),
    ]
    add_fieldsets = [
        (
            "Información personal",
            {
                "fields": [
                    "foto",
                    "nombre",
                    "correo_electronico",
                ],
            },
        ),
        (
            "Credenciales",
            {
                "fields": [
                    "usuario",
                    "password1",
                    "password2",
                ]
            },
        ),
        (
            "Permisos",
            {"fields": ["groups"]},
        ),
    ]
    search_fields = ["nombre", "usuario", "correo_electronico"]
    ordering = ["nombre"]
    filter_horizontal = []

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_superuser=False)

    @admin.display(description="activo")
    def is_active(self, instance):
        return instance.is_active


admin.site.register(IMAP)
admin.site.register(UsuarioIMAP)
