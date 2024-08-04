import os
import json
from django.core.management.base import BaseCommand
from item.models import Item, ItemMarketplace, Marketplace

class Command(BaseCommand):
    help = 'Update recommendations from a specified JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file with recommendations')

    def handle(self, *args, **options):
        json_file_path = options['json_file']

        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"File not found: {json_file_path}")

        def load_recommendations(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data

        def update_recommendations(data):
            for entry in data:
                product_name = entry['product_name']
                marketplace_name = entry['marketplace_name']
                average_rating = entry['average_rating']
                price = entry['price']

                item, created = Item.objects.get_or_create(name=product_name)
                marketplace, created = Marketplace.objects.get_or_create(name=marketplace_name)

                ItemMarketplace.objects.update_or_create(
                    item=item,
                    marketplace=marketplace,
                    defaults={
                        'marketplace_rating': average_rating,
                        'price': price
                    }
                )

        data = load_recommendations(json_file_path)
        update_recommendations(data)
        self.stdout.write(self.style.SUCCESS('Recommendations updated successfully'))

