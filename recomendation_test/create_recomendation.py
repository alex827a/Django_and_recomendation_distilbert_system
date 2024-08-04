import json
from transformers import DistilBertTokenizer, AutoModelForSequenceClassification
import torch
import time

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

def save_ratings_to_json(ratings):
    with open("all_products_ratings.json", 'w', encoding='utf-8') as f:
        json.dump(ratings, f, ensure_ascii=False, indent=4)

def main(json_file_path):
    start_time = time.time()  # Start timer
    products = load_reviews(json_file_path)
    ratings = []
    for product in products:
        product_name = product['name']
        reviews = [review['comment'] for review in product['reviews']]
        sentiments = analyze_sentiment(reviews)
        average_rating = calculate_average_rating(sentiments)
        ratings.append({
            "product_name": product_name,
            "average_rating": average_rating
        })
    save_ratings_to_json(ratings)
    end_time = time.time()  # Stop timer
    print("All Abarage ratings save in file.")
    print(f"Work done for {end_time - start_time:.2f} seonds.")

if __name__ == "__main__":
    json_file_path = "./products_and_reviews.json"
    main(json_file_path)
