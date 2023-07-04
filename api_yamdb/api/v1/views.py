from permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
)
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title

from .serializers import (
    CategorySerializer, GenreSerializer, TitleCreateSerializer,
    TitleShowSerializer,
)


class CategoryViewSet(CreateModelMixin,
                      DestroyModelMixin,
                      ListModelMixin):
    """Вьюсет для категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin):
    """Вьюсет для жанра."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведения."""

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    http_method_names = ('get', 'post', 'delete', 'patch')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleShowSerializer
        return TitleCreateSerializer
