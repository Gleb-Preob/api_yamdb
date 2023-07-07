from django.db.models import Avg
from django.shortcuts import get_object_or_404
from permissions import IsAdminOrReadOnly, IsAdminOwnerOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
)
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title, Review

from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleCreateSerializer, TitleShowSerializer,
    ReviewSerializer, CommentSerializer
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

    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('-pub_date')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    http_method_names = ('get', 'post', 'delete', 'patch')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleShowSerializer
        return TitleCreateSerializer


class ReviewViewSet(ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOwnerOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    """Вьюсет для комментариев на отзывы."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOwnerOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
