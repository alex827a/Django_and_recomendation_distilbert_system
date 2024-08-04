


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
Sentiment Analysis: Analyze sentiments for selected categories.  

## Project Structure
Main Automation Command: Orchestrates the entire process of fetching data, generating recommendations, and updating marketplace ratings.  
Individual Commands:  
'fetch_and_save_products': Fetches and stores product data.  
'create_recommendations': Generates product recommendations for each marketplace.  
'update_item_marketplace': Updates marketplace data from JSON files.  
'analyze_setiment_category': Analyzes sentiments for selected categories.  

### Running the Automation Command  
To run the main automation command and update the marketplace data, use the following command:  
```bash
python manage.py automatization_process --data-dir /path/to/your/data/directory  
```

#### This command will:  
Fetch and save product data.  
Create and update recommendations for each active marketplace.  
Update item marketplace data from the specified data directory.  
Update average ratings for items.  

## Admin Actions
Run Automatization Process: Triggers the entire automation process from the admin interface.  
Fetch Products: Fetches product data from an API.  
Activate/Deactivate Marketplaces: Activates or deactivates selected marketplaces.  
Update Average Ratings: Updates the average ratings for selected products.  
Create Recommendations: Creates and updates recommendations for selected marketplaces.  
Analyze Sentiments: Analyzes sentiments for selected categories.  

## Configuration
Data Directory: Specify the directory where JSON files with marketplace data are stored using the `--data-dir` option.  
Marketplace Names: Ensure that the marketplace names used in the JSON files match the names configured in the Django admin.  

### Example JSON File Structure
Each JSON file should be named in the format `{marketplace_name}_ratings.json` and contain the relevant data for that marketplace.  

## Jupyter Notebook for DistilBert Electronics Sentiment  
In my pretrained model I used the Electronics dataset from Amazon. You can download many other datasets from here:  
https://jmcauley.ucsd.edu/data/amazon/  
You also can download my test model on HuggingFace. Add this model in \recomendation_test\final_model3
alexot/DistilBert_Classification_Electronics
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



## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact
For any inquiries or support, please open an issue or contact [alexot422@gmail.com](mailto:alexot422@gmail.com).

