from django.contrib.auth.base_user import BaseUserManager


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, usuario, password, **kwargs):
        if not usuario:
            raise ValueError("El nombre de usuario es requerido.")
        user = self.model(usuario=usuario, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, usuario, password=None, **kwargs):
        data = kwargs.copy()
        data["is_superuser"] = False
        return self._create_user(usuario, password, **kwargs)

    def create_superuser(self, usuario, password, **kwargs):
        data = kwargs.copy()
        data["is_superuser"] = True
        return self._create_user(usuario, password, **data)
