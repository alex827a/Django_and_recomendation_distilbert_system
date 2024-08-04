from django.core.management.base import BaseCommand
from recomendation_test.create_recomandation_category import main  # Import main

class Command(BaseCommand):
    help = 'Analyzes sentiments for a given category'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to the JSON file with product data')
        parser.add_argument('category', type=str, help='Category name to analyze')

    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        category = options['category']
        main(json_file_path, category)  # Call main
        self.stdout.write(self.style.SUCCESS(f"Sentiment analysis completed for category {category}"))
