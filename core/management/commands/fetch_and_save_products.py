from django.core.management.base import BaseCommand
from django.contrib import messages
from item.models import Marketplace
import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch and save product data with marketplace info and reviews'

    def add_arguments(self, parser):
        parser.add_argument('--noinput', '--no-input', action='store_false', help="Do not prompt for input of any kind.")

    def handle(self, *args, **options):
        active_marketplaces = Marketplace.objects.filter(is_active=True)
        if not active_marketplaces.exists():
            logger.error('No active marketplaces configured.')
            self.stdout.write(self.style.ERROR('No active marketplaces configured.'))
            return

        for marketplace in active_marketplaces:
                #Get data from database for asces 
            logger.info(f"Fetching data for marketplace: {marketplace.name}")
            headers = {'Authorization': f'Token {marketplace.token}'}
            try:
                response = requests.get(marketplace.api_url, headers=headers)
                response.raise_for_status()  # Check errors  HTTP
                logger.info(f"Successfully fetched data for {marketplace.name}")
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP Error for {marketplace.name}: {e}")
                self.stdout.write(self.style.ERROR(f"HTTP Error for {marketplace.name}: {e}"))
                continue
            except requests.exceptions.ConnectionError:
                logger.error(f"Connection Error for {marketplace.name}")
                self.stdout.write(self.style.ERROR(f"Connection Error for {marketplace.name}"))
                continue
            except requests.exceptions.Timeout:
                logger.error(f"Timeout Error for {marketplace.name}")
                self.stdout.write(self.style.ERROR(f"Timeout Error for {marketplace.name}"))
                continue
            except requests.exceptions.RequestException as e:
                logger.error(f"Unexpected Error for {marketplace.name}: {e}")
                self.stdout.write(self.style.ERROR(f"Unexpected Error for {marketplace.name}: {e}"))
                continue

            products = response.json()
            logger.info(f"Number of products fetched for {marketplace.name}: {len(products)}")
            for product in products:
                product['marketplace_name'] = marketplace.name
                product['marketplace_url'] = marketplace.url

            file_path = os.path.join(os.getcwd(), 'recomendation_test', f"{marketplace.name}_products_and_reviews.json")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=4)
            logger.info(f'Successfully fetched and stored product data for {marketplace.name}.')
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched and stored product data for {marketplace.name}.'))

        self.stdout.write(self.style.SUCCESS('Operation completed. Check the log for details.'))
