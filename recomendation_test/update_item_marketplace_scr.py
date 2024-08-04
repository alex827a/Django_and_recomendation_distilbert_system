from item.models import Category, Item, Marketplace, ItemMarketplace
import json
import os
def update_item_marketplace(data):
    for entry in data:
        item_name = entry['product_name']
        marketplace_name = entry['marketplace_name']
        marketplace_url = entry['marketplace_url']  # URL marketplace with JSON
        category_name = entry.get('category_name', 'Default Category')
        average_rating = entry['average_rating']
        price = entry.get('price')

        # Get or create object Category
        category, cat_created = Category.objects.get_or_create(
            name=category_name
        )

        # Get or create object Item with new or finding categorie
        item, item_created = Item.objects.get_or_create(
            name=item_name,
            defaults={
                'description': entry.get('description', ''),
                'price': entry.get('price', 0),
                'category': category
            }
        )
        
        # Get or create Marketplace with URL
        marketplace, mkt_created = Marketplace.objects.get_or_create(
            name=marketplace_name,
            defaults={'url': marketplace_url}
        )

        # Create or update ItemMarketplace
        item_marketplace, imp_created = ItemMarketplace.objects.update_or_create(
            item=item,
            marketplace=marketplace,
            defaults={'marketplace_rating': average_rating, 'price': price}
        )

        print(f"{'Created new' if cat_created else 'Updated'} category: {category.name}")
        print(f"{'Created new' if item_created else 'Updated'} item: {item.name}")
        print(f"{'Created new' if mkt_created else 'Updated'} marketplace: {marketplace.name} with URL {marketplace_url}")
        print(f"{'Created new' if imp_created else 'Updated'} item_marketplace for {item.name} at {marketplace.name}")






def load_data_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

