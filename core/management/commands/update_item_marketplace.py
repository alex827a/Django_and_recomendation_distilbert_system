from django.core.management.base import BaseCommand
from recomendation_test.update_item_marketplace_scr import update_item_marketplace, load_data_from_json
import os

class Command(BaseCommand):
    help = 'Update item marketplace data'

    # Добавляем аргументы команды
    def add_arguments(self, parser):
        parser.add_argument('marketplace_name', type=str, help='Marketplace name for which to update products')
        parser.add_argument('--data-dir', type=str, help='Directory where the data files are located', default='.')

    def handle(self, *args, **options):
        marketplace_name = options['marketplace_name']  # Получаем имя маркетплейса из опций команды
        data_dir = options['data_dir']  # Получаем путь к директории с данными
        data_file_path = os.path.join(data_dir, f"{marketplace_name}_ratings.json")  # Формируем полный путь к файлу данных

        # Печатаем отладочную информацию
        self.stdout.write(self.style.SUCCESS(f'Checking for data file at: {data_file_path}'))
        self.stdout.write(self.style.SUCCESS(f'Contents of directory: {os.listdir(data_dir)}'))

        # Проверка на существование файла
        if not os.path.exists(data_file_path):
            self.stdout.write(self.style.ERROR(f'Data file not found: {data_file_path}'))
            return

        # Загружаем данные из файла
        data = load_data_from_json(data_file_path)
        update_item_marketplace(data)  # Обновляем данные в базе
        self.stdout.write(self.style.SUCCESS(f'Data has been successfully updated for {marketplace_name}'))
