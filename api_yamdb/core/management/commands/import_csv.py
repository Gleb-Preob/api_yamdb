import csv
import sqlite3

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Imports .csv data to DB'

    FILES_NAMES = {
        'category.csv': 'reviews_category',
        'comments.csv': 'reviews_comment',
        'genre.csv': 'reviews_genre',
        'genre_title.csv': 'reviews_title_genre',
        'review.csv': 'reviews_review',
        'titles.csv': 'reviews_title',
        'users.csv': 'users_user',
    }
    DB_PATH = settings.DATABASES['default']['NAME']

    def handle(self, *args, **options):
        csv_root = settings.BASE_DIR/'static'/'data'
        files_paths = list(csv_root.glob('*.csv'))
        for file_path in files_paths:
            self.import_to_db(file_path)

    def import_to_db(self, file_path):
        connection = sqlite3.connect(self.DB_PATH)
        cursor = connection.cursor()

        with open(file_path, newline='', encoding='utf-8') as csv_file:
            dict_reader = csv.DictReader(csv_file)
            db = [i for i in dict_reader]

        table_keys = db[0].keys()
        values_query = self.make_values_query(table_keys)
        current_table = self.FILES_NAMES[file_path.name]
        table_fields = ', '.join(table_keys)

        cursor.executemany(
            (
                f'INSERT INTO {current_table}({table_fields}) '
                f'VALUES ({values_query});'
            ),
            db,
        )
        connection.commit()
        connection.close()

    @staticmethod
    def make_values_query(table_keys):
        result = ''
        for key in table_keys:
            result += f':{key}, '
        return result[:-2]
