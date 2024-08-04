from django.core.management.base import BaseCommand
from item.models import Item

class Command(BaseCommand):
    help = 'Update average ratings for all items based on marketplace ratings'

    def handle(self, *args, **kwargs):
        items = Item.objects.all()
        for item in items:
            item.update_average_rating()
            self.stdout.write(self.style.SUCCESS(f'Updated average rating for item {item.name}'))
