import csv
import os
import sqlite3

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User,
)


class Command(BaseCommand):
    help = 'Imports .csv data to DB'

    FILE_TO_MODEL = {
        'category.csv': Category,
        'genre.csv': Genre,
        'titles.csv': Title,
        'genre_title.csv': GenreTitle,
        'users.csv': User,
        'review.csv': Review,
        'comments.csv': Comment,
    }

    ALIAS_FOR_FIELDS = {
        'category': 'category_id',
        'author': 'author_id',
    }

    CSV_PATH = os.path.join(settings.BASE_DIR, 'static/data')

    DB_PATH = settings.DATABASES['default']['NAME']

    def read_csv(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            csv_file_headers = next(csv.reader(file))
            headers = []
            for header in csv_file_headers:
                if header in self.ALIAS_FOR_FIELDS:
                    headers.append(self.ALIAS_FOR_FIELDS[header])
                else:
                    headers.append(header)
            return list(csv.DictReader(file, fieldnames=headers))

    def load_csv(self, data, model):
        for row in data:
            model.objects.create(**row)

    def handle(self, *args, **options):
        for file_name, model in self.FILE_TO_MODEL.items():
            file_path = os.path.join(self.CSV_PATH, file_name)
            data = self.read_csv(file_path)
            self.load_csv(data, model)

        # во время миграции службной модели,
        # которая создалась для реализации связи
        # title_genre, создалась таблица genretitle.
        # иного способа, кроме нижеизложенного,
        # для заполнения title_genre не придумали

        connection = sqlite3.connect(self.DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO reviews_title_genre(id, title_id, genre_id),
        SELECT *,
        FROM reviews_genretitle;
        ''')

        connection.commit()
        connection.close()
