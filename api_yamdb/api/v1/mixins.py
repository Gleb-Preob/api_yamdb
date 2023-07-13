from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet


class PatchModelMixin(UpdateModelMixin):

    @swagger_auto_schema(auto_schema=None)
    def update(self, *args, **kwargs):
        raise MethodNotAllowed('PUT', detail='Недопустимый метод PUT')

    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs, partial=True)


class PutDenyMixin(
    GenericViewSet,
    PatchModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin
):

    pass


class DestroyCreateListMixin(
    GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
):

    pass
