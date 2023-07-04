from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
