from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    permisos = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ["foto", "nombre", "usuario", "correo_electronico", "permisos"]

    def get_permisos(self, instance):
        result = {}
        permissions = instance.get_all_permissions()
        for _permission in permissions:
            app, permission = _permission.split(".")
            action, model = permission.split("_")
            if app not in result:
                result[app] = {}
            if model not in result[app]:
                result[app][model] = []
            result[app][model].append(action)
        return result


class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    contrasena = serializers.CharField()


class TokenObtainPairSerializer_(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["usuario"] = UsuarioSerializer(self.user, context=self.context).data
        return data

    # TODO: registrar una `issue` de poder cambiar el nombre del campo de la contraseña.
    def to_internal_value(self, data):
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        data["password"] = data.pop("contrasena")
        return data


class TokenRefreshSerializer_(TokenRefreshSerializer):
    pass
