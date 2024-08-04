import os
import json
import argparse
from django.core.management.base import BaseCommand
from transformers import DistilBertTokenizer, AutoModelForSequenceClassification
import torch
import time
from item.models import Item, Marketplace, ItemMarketplace

class Command(BaseCommand):
    help = 'Create and update recommendations for a selected marketplace'

    def add_arguments(self, parser):
        parser.add_argument('marketplace_name', type=str, help='Marketplace name for which to create recommendations')
        parser.add_argument('--category', type=str, default=None, help='Category name to analyze (optional)')

    def handle(self, *args, **options):
        marketplace_name = options['marketplace_name']
        category = options['category']

        model_path = os.path.abspath("E:/django_diplom_arbeit/сompareshop/recomendation_test/final_model3")

        # Check route in model
        if not os.path.exists(model_path):
            raise ValueError(f"Model path not found: {model_path}")

        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        def load_reviews(json_file_path):
            if not os.path.exists(json_file_path):
                raise FileNotFoundError(f"File not found: {json_file_path}")

            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data

        def analyze_sentiment(reviews):
            sentiments = []
            for review in reviews:
                inputs = tokenizer(review, return_tensors="pt", padding=True, truncation=True)
                with torch.no_grad():
                    outputs = model(**inputs)
                    predictions = torch.argmax(outputs.logits, dim=1)
                    adjusted_sentiment = predictions.item() + 1
                    sentiments.append(adjusted_sentiment)
            return sentiments

        def calculate_average_rating(sentiments):
            if sentiments:
                return sum(sentiments) / len(sentiments)
            else:
                return 0

        def save_ratings_to_json(ratings, marketplace_name, category_name=None):
            if category_name:
                category_file_name = f"{marketplace_name}_{category_name}_ratings.json"
                category_file_path = os.path.join("ratings", category_file_name)
                os.makedirs(os.path.dirname(category_file_path), exist_ok=True)
                with open(category_file_path, 'w', encoding='utf-8') as f:
                    json.dump(ratings, f, ensure_ascii=False, indent=4)
                print(f"Avarage rating for categotys {category_name} in {marketplace_name} saved in file {category_file_name}.")
            else:
                general_file_name = f"{marketplace_name}_ratings.json"
                general_file_path = os.path.join("ratings", general_file_name)
                os.makedirs(os.path.dirname(general_file_path), exist_ok=True)
                with open(general_file_path, 'w', encoding='utf-8') as f:
                    json.dump(ratings, f, ensure_ascii=False, indent=4)
                print(f"Avarage ratings for  {marketplace_name} saved in file {general_file_name}.")

        def main(marketplace_name, category=None):
            #Change path im your directory
            json_file_path = os.path.abspath(f"E:/django_diplom_arbeit/сompareshop/recomendation_test/{marketplace_name}_products_and_reviews.json")
            if not os.path.exists(json_file_path):
                raise FileNotFoundError(f"File not found: {json_file_path}")

            start_time = time.time()
            products = load_reviews(json_file_path)
            ratings = []
            for product in products:
                if not category or product.get('category_name') == category:
                    product_name = product['name']
                    product_category = product.get('category_name', 'General')
                    product_price = product.get('price', 0)
                    reviews = [review['comment'] for review in product['reviews']]
                    sentiments = analyze_sentiment(reviews)
                    average_rating = calculate_average_rating(sentiments)
                    ratings.append({
                        "product_name": product_name,
                        "category_name": product_category,
                        "average_rating": average_rating,
                        "price": product_price,
                        "marketplace_name": marketplace_name,
                        "marketplace_url": product.get('marketplace_url', 'No URL provided')
                    })
            save_ratings_to_json(ratings, marketplace_name, category)
            end_time = time.time()
            print(f"Procces complieted for {end_time - start_time:.2f} second.")

        main(marketplace_name, category)
