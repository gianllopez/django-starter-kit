import datetime
from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from imbox import Imbox


class SMTP:
    """Encargada del envío de correos electrónicos.

    Args:
        template (str): plantilla a cargar, ubicada en `/assets/templates/`.
        subject (str): asunto del correo electrónico.
        to (list(str)): direcciones de correo electrónico donde se va a enviar.

    Attributes:
        email (EmailMultiAlternatives): instancia del correo electrónico a enviar.
    """

    def __init__(self, template, subject, to, *args, **kwargs):
        context = kwargs.get("context", {})
        html = loader.render_to_string(template, context=context)

        email = EmailMultiAlternatives(
            subject=subject,
            to=to,
            body=html,
            from_email=settings.EMAIL_HOST_USER,
            *args,
            **kwargs,
        )
        email.content_subtype = "html"
        email.mixed_subtype = "related"

        logo = MIMEImage(open("assets/logo.png", "rb").read())
        logo.add_header("Content-ID", "<logo>")
        email.attach(logo)

        self.email = email

    def send(self, *args, **kwargs):
        """Envía el correo electrónico.

        Returns:
            int: 1 si el correo se envió, 0 si no.
        """
        return self.email.send(*args, **kwargs)


class IMAP:
    """Encargada de la lectura de la bandeja de correos electrónicos.

    Args:
        user (apps.usuarios.models.Usuario): usuario con la bandeja a leer.

    Attributes:
        imbox (imbox.Imbox): encargada de la conexión con la bandeja.
    """

    def __init__(self, user):
        imap = user.IMAP.get(activo=True)
        server = imap.servidor
        self.imbox = Imbox(
            hostname=server.hostname,
            port=server.puerto,
            username=imap.servidor_usuario,
            password=imap.servidor_contrasena,
        )

    def recents(self):
        """Regresa los correos electrónicos no leídos y desde un día anterior.

        Returns:
            list: correos electrónicos recientes ya parseados.
        """
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        emails = self.imbox.messages(unread=True, date__gt=yesterday)
        return self.response(emails)

    def response(self, emails):
        """Parsea los correos electrónicos devueltos.

        Args:
            emails (imbox.Messages): lista con los correos electrónicos devueltos por `imbox.Imbox()`.

        Returns:
            list: correos electrónicos parseados.
        """
        parsed_emails = []
        for _, email in emails:
            sender = email.sent_from
            date = email.parsed_date.strftime("%d/%m/%Y %I:%M %p")
            if len(sender) > 0:
                sender = sender[0]
                initials = self.get_sender_initials(sender)
                parsed_emails.append(
                    {
                        "asunto": email.subject,
                        "fecha": date,
                        "remitente": {
                            "nombre": sender["name"],
                            "correo_electronico": sender["email"],
                            "iniciales": initials,
                        },
                    }
                )
        return parsed_emails

    def get_sender_initials(self, sender: dict[str, str]) -> str:
        """Construye las iniciales del emisor de un correo electrónico.

        Args:
            sender (dict): información del emisor.

        Returns:
            str: iniciales del emisor.
        """
        name = sender["name"]
        initials = sender["email"].split("@")[0][:2]
        if name != "":
            name_list = name.split(" ")
            if len(name_list) >= 3:
                initials = "".join([name[0] for name in name_list[:1] + name_list[2:3]])
        return initials.upper()
