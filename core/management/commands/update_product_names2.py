import re
from django.core.management.base import BaseCommand
from item.models import Item
import os

class Command(BaseCommand):
    help = 'Update product names from a text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the text file containing product names')

    def clean_name(self, name):
        # Удаляем специальные символы и лишние пробелы
        return re.sub(r'[^\w\s]', '', name).strip()

    def handle(self, *args, **options):
        file_path = options['file_path']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('File does not exist'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            new_names = [self.clean_name(name) for name in content.split(';') if name.strip()]

        # Update product names
        for item, new_name in zip(Item.objects.all().order_by('id'), new_names):
            # Сравнение чистых имен
            cleaned_item_name = self.clean_name(item.name)
            if cleaned_item_name == new_name:
                item.name = new_name
                item.save()
                self.stdout.write(self.style.SUCCESS(f'Updated product {item.id} name to {new_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Name does not match for ID {item.id}: {item.name}'))

        self.stdout.write(self.style.SUCCESS('All applicable product names updated successfully'))

