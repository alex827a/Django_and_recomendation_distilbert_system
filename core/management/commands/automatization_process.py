from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.models import Avg
from item.models import Marketplace, Item

class Command(BaseCommand):
    help = 'Automate the process of fetching data, creating recommendations, and updating marketplace ratings'

    def add_arguments(self, parser):
        parser.add_argument('--data-dir', type=str, help='Directory where the data files are located', default='.')

    def handle(self, *args, **options):
        data_dir = options['data_dir']  # Get path for directory

        # Step 1: Fetch and save products
        self.stdout.write(self.style.SUCCESS('Fetching and saving product data...'))
        call_command('fetch_and_save_products')

        # Step 2: Create and update recommendations
        active_marketplaces = Marketplace.objects.filter(is_active=True)
        if not active_marketplaces.exists():
            self.stdout.write(self.style.ERROR('No active marketplaces configured.'))
            return

        for marketplace in active_marketplaces:
            self.stdout.write(self.style.SUCCESS(f'Creating recommendations for {marketplace.name}...'))
            call_command('create_recommendations', marketplace.name)

        # Step 3: Update item marketplace data
        self.stdout.write(self.style.SUCCESS('Updating item marketplace data...'))
        for marketplace in active_marketplaces:
            self.stdout.write(self.style.SUCCESS(f'Updating item marketplace data for {marketplace.name}...'))
            self.stdout.write(self.style.SUCCESS(f'Calling update_item_marketplace with data_dir={data_dir}'))
            try:
                call_command('update_item_marketplace', marketplace_name=marketplace.name, data_dir=data_dir)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating marketplace data: {e}'))

        # Step 4: Update average ratings for items
        self.stdout.write(self.style.SUCCESS('Updating average ratings for items...'))
        items = Item.objects.all()
        for item in items:
            marketplace_ratings = item.marketplaces.all()
            if marketplace_ratings.exists():
                average_rating = marketplace_ratings.aggregate(Avg('marketplace_rating'))['marketplace_rating__avg']
                item.average_rating = average_rating
                item.save()
            else:
                item.average_rating = None
                item.save()

        self.stdout.write(self.style.SUCCESS('Automatization process completed successfully.'))
