import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import schedule  # type: ignore

HEADERS = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
]

def scrape_reviews(url, pages=3):
    """ Scrapes product reviews dynamically. """
    reviews = []
    
    for page in range(1, pages + 1):
        full_url = f"{url}&pageNumber={page}"
        headers = random.choice(HEADERS)

        response = requests.get(full_url, headers=headers)
        if response.status_code != 200:
            print(f"⚠️ Failed to retrieve page {page}, Status Code: {response.status_code}")
            time.sleep(random.uniform(5, 10))  # Avoid bot detection
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        review_elements = soup.find_all('div', {'data-hook': 'review'})

        for review in review_elements:
            try:
                review_text = review.find('span', {'data-hook': 'review-body'}).text.strip()
                rating = float(review.find('i', {'data-hook': 'review-star-rating'}).text.split()[0])

                reviews.append({'review_text': review_text, 'rating': rating})
            except AttributeError:
                continue

        print(f"Scraped page {page}")
        time.sleep(random.uniform(3, 7)) 

    return reviews

def update_real_time_feed():
    product_urls = [
        "https://www.amazon.com/product-reviews/B07N47M28M",  
    ]

    all_reviews = []
    for url in product_urls:
        reviews = scrape_reviews(url)
        all_reviews.extend(reviews)

    df = pd.DataFrame(all_reviews)
    df.to_csv("real_time_reviews.csv", index=False)
    print("Real-time feed updated.")

schedule.every(30).minutes.do(update_real_time_feed)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)