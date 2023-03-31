from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = "Create a superuser with a password non-interactively"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--contrasena",
            dest="contrasena",
            default=None,
            help="Especifica la contraseña del usuario.",
        )
        parser.add_argument(
            "--correo_electronico",
            dest="correo_electronico",
            default=None,
            help="Especifica el correo electrónico del usuario.",
        )

    def handle(self, *args, **options):
        options.setdefault("interactive", False)
        database = options.get("database")
        contrasena = options.get("contrasena")
        usuario = options.get("usuario")
        correo_electronico = options.get("correo_electronico")

        if not contrasena or not usuario or not correo_electronico:
            raise CommandError(
                "--usuario, --contrasena y --correo_electronico son requeridos."
            )

        self.UserModel._default_manager.db_manager(database).create_superuser(
            usuario=usuario, password=contrasena, correo_electronico=correo_electronico
        )

        if options.get("verbosity", 0) >= 1:
            self.stdout.write(
                self.style.SUCCESS("* Usuario administrador creado correctamente.")
            )
