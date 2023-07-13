import datetime as dt

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameRegexValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя."""

    regex = r'^[\w.@+-]+\Z'
    flags = 0
    max_length = settings.LEN_DATA_USER
    message = ('Введите правильное имя пользователя. Оно может содержать'
               ' только буквы, цифры и знаки @/./+/-/_.'
               f' Длина не более {settings.LEN_DATA_USER} символов')
    error_messages = {
        'invalid': f'Набор символов не более {settings.LEN_DATA_USER}. '
                   'Только буквы, цифры и @/./+/-/_',
        'required': 'Поле не может быть пустым',
    }


def validate_year(year):
    current_day = dt.date.today()
    if year > current_day.year:
        raise ValidationError('Вы не Марти Макфлай!'
                              'Год не должен быть из будущего!')
