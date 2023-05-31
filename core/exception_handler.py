from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            detail = response.data.pop("detail")
            response.data = {"message": str(detail), "code": detail.code}
    return response
