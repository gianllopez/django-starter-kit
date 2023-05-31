from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.helpers.email import IMAP, SMTP

from .models import Usuario
from .serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.filter(is_superuser=False)
    serializer_class = UsuarioSerializer

    @action(detail=False)
    def whoami(self, request):
        context = self.get_serializer_context()
        data = UsuarioSerializer(request.user, context=context).data
        return Response(data)

    @action(detail=False)
    def bandeja(self, request):
        inbox = IMAP(request.user)
        recents = inbox.recents()
        return Response(recents)

    @action(detail=False)
    def smtp(self, _):
        config = {
            "template": "email.base.html",
            "subject": "THIS IS A TEST",
            "to": ["test@thisisatest.test"],
        }
        smtp = SMTP(**config)
        config["sent"] = smtp.send()
        return Response(config)
