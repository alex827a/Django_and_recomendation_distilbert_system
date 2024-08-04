from django.core.management.base import BaseCommand
from item.models import Item, User, Category
import random
import decimal

class Command(BaseCommand):
    help = 'Generate random products in the database'

    def add_arguments(self, parser):
        parser.add_argument('num_products', type=int, help='Number of products to create')
        parser.add_argument('username', type=str, help='Username of the product creator')
        parser.add_argument('category_id', type=int, help='Category ID for the products')

    def handle(self, *args, **options):
        num_products = options['num_products']
        username = options['username']
        category_id = options['category_id']

        # Searching user by  username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with username {username} not found'))
            return

        #Seraching category by ID
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Category with ID {category_id} not found'))
            return
        
        for _ in range(num_products):
            name = f'Product {_ + 1}'
            description = f'Description for Product {_ + 1}'
            price = decimal.Decimal(random.randrange(100, 10000))/100
            Item.objects.create(
                name=name,
                description=description,
                price=price,
                created_by=user,
                category=category  
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_products} products by {username} in category {category.name}'))
     