import json
import re
from django.core.management.base import BaseCommand
from item.models import Item

class Command(BaseCommand):
    help = 'Update product ratings from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing product ratings')

    def clean_name(self, name):
        # Удаляем специальные символы и исправляем кодировочные артефакты, оставляя запятые, круглые скобки и вертикальные черты
      # Удаление символов ®, ™ и артефактов кодировки
        # Удаление всех нежелательных символов, кроме буквенно-цифровых, пробелов, запятых, круглых скобок и вертикальных черт, которые не идут подряд
          # Заменяем последовательные вертикальные черты на одну
        return name.strip()

    def handle(self, *args, **options):
        with open(options['json_file'], 'r', encoding='utf-8') as file:
            products_data = json.load(file)

        for product in products_data:
            product_name = self.clean_name(product['product_name'])
            average_rating = product['average_rating']

            # Находим товар по названию после очистки
            try:
                item = Item.objects.get(name__iexact=product_name)
                item.average_rating = average_rating
                item.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated {product_name} with average rating of {average_rating}'))
            except Item.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Item with name "{product_name}" not found'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating {product_name}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('All product ratings updated successfully'))
