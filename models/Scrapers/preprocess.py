import pandas as pd
import re
import string

df = pd.read_csv("../data/product_reviews.csv")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text) 
    text = text.translate(str.maketrans('', '', string.punctuation)) 
    text = text.strip()
    return text

df["cleaned_review"] = df["review_text"].apply(clean_text)

df.to_csv("../data/cleaned_product_reviews.csv", index=False)
print("Data Cleaning Complete!")