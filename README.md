# Marketplace Automation Project
## Overview
The Marketplace Automation Project is a Django-based application designed to streamline the process of fetching product data, generating recommendations,
and updating marketplace ratings. This project leverages Django management commands to automate these tasks, making it easier to maintain and enhance product 
listings and recommendations across various marketplaces.  

## Features
Automated Data Fetching: Retrieve and save product data from various sources.  
Recommendation Generation: Create personalized recommendations for products in each marketplace.  
Marketplace Data Update: Update product data and ratings for each marketplace.  
Rating Calculation: Compute and update average ratings for products based on marketplace data.  


## Project Structure
Main Automation Command: Orchestrates the entire process of fetching data, generating recommendations, and updating marketplace ratings.  
Individual Commands:  
'fetch_and_save_products': Fetches and stores product data.  
'create_recommendations': Generates product recommendations for each marketplace.  
'update_item_marketplace': Updates marketplace data from JSON files. 
 
### Running the Automation Command  
To run the main automation command and update the marketplace data, use the following command:    
python manage.py automate_marketplace --data-dir /path/to/your/data/directory  

#### This command will:  
Fetch and save product data.  
Create and update recommendations for each active marketplace.  
Update item marketplace data from the specified data directory.  
Update average ratings for items.  


## Jupyter Noyebook for DistilBert electronics sentiment  
In my pretrained model i used Elctronic dataset from amazon you can download here many other datasets  
https://jmcauley.ucsd.edu/data/amazon/
### Used Libraries:
os  
nltk  
seaborn  
pandas  
matplotlib.pyplot  
docx.shared  
sklearn.model_selection  
torch  
numpy  
transformers  
sklearn.metrics  
