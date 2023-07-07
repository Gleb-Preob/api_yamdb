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

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Вьюсет для комментариев на отзывы."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOwnerOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
