import os
import requests
import json
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetch and save product data with marketplace info and reviews'

    def handle(self, *args, **options):
        token = 'd8b9d3ef06bd1d3f19c8bb1bf34b11a13c759e19'  # Use environment variables or secure means to store token
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://127.0.0.1:8080/api/products/', headers=headers)

        if response.status_code == 200:
            products = response.json()

            # Добавление информации о маркетплейсе для каждого продукта
            for product in products:
                product['marketplace_name'] = 'Marketplace_one'
                product['marketplace_url'] = 'http://127.0.0.1:8080'  # Замените на актуальное название маркетплейса

            # Определение пути к папке и файлу
            file_path = os.path.join(settings.BASE_DIR, 'recomendation_test', 'products_and_reviews.json')
            data_dir = os.path.join(settings.BASE_DIR, 'recomendation_test')
            os.makedirs(data_dir, exist_ok=True)

            # Сохранение данных в UTF-8
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=4)
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored product data with reviews and manually added marketplace info.'))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch products. Status: {response.status_code}"))
            self.stdout.write(self.style.ERROR(response.text))
