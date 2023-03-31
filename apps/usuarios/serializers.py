from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["nombre", "apellido", "usuario", "correo_electronico"]


class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    contrasena = serializers.CharField()


class TokenObtainPairSerializer_(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return {**data, "usuario": UsuarioSerializer(self.user).data}

    def to_internal_value(self, data):
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data.copy()
        data["password"] = data.pop("contrasena", None)
        return data


class TokenRefreshSerializer_(TokenRefreshSerializer):
    pass
