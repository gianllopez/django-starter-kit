from django import forms
from django.contrib.auth import get_user_model


class UsuarioForm(forms.ModelForm):
    password = password = forms.CharField(
        widget=forms.PasswordInput, label="Contraseña"
    )

    class Meta:
        model = get_user_model()
        fields = ["nombre", "apellido", "usuario", "correo_electronico", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
