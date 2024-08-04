import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Automates the process of fetching data, creating recommendations, and updating ratings.'

    def handle(self, *args, **options):
        # Step 1:Get data from marketplaces
        self.stdout.write(self.style.SUCCESS('Starting data fetching...'))
        call_command('get_data')
        self.stdout.write(self.style.SUCCESS('Data fetching completed successfully.'))

        # Step 2: Create recomendations
        self.stdout.write(self.style.SUCCESS('Creating recommendations...'))
        os.chdir('recomendation_test')  # Go to directory
        os.system('python create_recomendation.py')
        os.chdir('../')  # Return in main directory
        self.stdout.write(self.style.SUCCESS('Recommendations created successfully.'))

        # Step 3: Update ratings
        self.stdout.write(self.style.SUCCESS('Updating product ratings...'))
        call_command('update_ratings', 'recomendation_test/all_products_ratings.json')
        self.stdout.write(self.style.SUCCESS('Product ratings updated successfully.'))

        # Final messages
        self.stdout.write(self.style.SUCCESS('All processes completed successfully.'))
