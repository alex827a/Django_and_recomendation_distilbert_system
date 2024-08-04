import json
import argparse
from transformers import DistilBertTokenizer, AutoModelForSequenceClassification
import torch
import time, os

model_path = "./final_model3"
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def load_reviews(json_file_path):
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

def save_ratings_to_json(ratings, category_name):
    file_name = f"{category_name}_category_ratings.json"
    file_path = os.path.join("ratings", file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(ratings, f, ensure_ascii=False, indent=4)

def main(json_file_path, category):
    start_time = time.time()
    products = load_reviews(json_file_path)
    ratings = []
    for product in products:
        if product.get('category_name') == category:
            product_name = product['name']
            marketplace_name = product.get('marketplace_name', 'Unknown')  # Default to 'Unknown' if not provided
            marketplace_url = product.get('marketplace_url', 'No URL provided')  # Default to placeholder
            reviews = [review['comment'] for review in product['reviews']]
            sentiments = analyze_sentiment(reviews)
            average_rating = calculate_average_rating(sentiments)
            ratings.append({
                "product_name": product_name,
                "category_name": category,
                "average_rating": average_rating,
                "marketplace_name": marketplace_name,
                "marketplace_url": marketplace_url
            })
    save_ratings_to_json(ratings, category)
    end_time = time.time()
    print(f"Avg retings category '{category}' save in file {category}_category_ratings.json.")
    print(f"Work done for {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze sentiment for reviews of products in a specific category.')
    parser.add_argument('json_file_path', type=str, help='Path to the JSON file with product data')
    parser.add_argument('category', type=str, help='Category name to analyze')
    args = parser.parse_args()
    main(args.json_file_path, args.category)
