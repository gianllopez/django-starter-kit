from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from .models import Usuario


class GrupoForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.exclude(
            content_type__app_label__in=[
                "auth",
                "admin",
                "sessions",
                "contenttypes",
            ]
        ),
        label="Permisos",
        widget=FilteredSelectMultiple("grupos", False),
    )

    class Meta:
        model = Group
        fields = "__all__"


class CrearUsuarioForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        Group.objects.all(),
        label="Grupos",
        widget=FilteredSelectMultiple("grupos", False),
    )

    class Meta:
        model = Usuario
        fields = ["foto", "nombre", "usuario", "correo_electronico"]
        labels = {"correo_electronico": "Correo electrónico"}


class ActualizarUsuarioForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ["foto", "nombre", "usuario", "correo_electronico", "password"]
        labels = {"correo_electronico": "Correo electrónico"}
