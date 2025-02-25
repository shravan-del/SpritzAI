import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_amazon_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }  # Setting user-agent to mimic a browser

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract review data
        reviews = []
        review_elements = soup.find_all('div', {'data-hook': 'review'})
        for review in review_elements:
            # Extract review text
            review_text = review.find('span', {'data-hook': 'review-body'}).text.strip()
            
            # Extract star rating (you might need to adjust this based on the actual HTML structure)
            rating = review.find('i', {'data-hook': 'review-star-rating'}).text.split()[0]
            
            # Optionally, you can scrape reviewer name, date, etc., if needed
            reviews.append({
                'review_text': review_text,
                'rating': float(rating)
            })
        
        return reviews
    else:
        print('Failed to retrieve the webpage')
        return None

# Example URL, replace with actual product review page
url = 'https://www.amazon.com/product-reviews/B07N47M28M/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
reviews = scrape_amazon_reviews(url)

if reviews:
    df = pd.DataFrame(reviews)
    print(df.head())  # View the first few entries
    
    # Save to CSV
    df.to_csv('reviews.csv', index=False)
else:
    print("No reviews were scraped.")