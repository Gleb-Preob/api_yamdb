from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review, Comment, User
from reviews.validators import UsernameRegexValidator


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleShowSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        read_only=True,
        source='reviews__score__avg'
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        view = self.context.get('view')
        author = request.user
        title = get_object_or_404(Title, id=view.kwargs.get('title_id'))

        if (title.reviews.filter(author=author).exists()
           and request.method == 'POST'):
            raise serializers.ValidationError(
                'Вы уже отправляли отзыв на это произведение. '
                'Возможно составить только один отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UsernameRegexValidator()
        ],
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        max_length=254,
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UsernameRegexValidator(), ]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=(UsernameRegexValidator(),)
    )
    confirmation_code = serializers.CharField(
        required=True
    )
