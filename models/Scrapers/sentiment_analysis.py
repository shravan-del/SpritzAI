import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd

tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = BertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment", num_labels=5)

def analyze_sentiment(text):
    """ Returns a sentiment score (1-5) based on the review text. """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    outputs = model(**inputs)
    sentiment_score = torch.argmax(outputs.logits).item() + 1  
    return sentiment_score

def score_real_time_reviews():
    df = pd.read_csv("real_time_reviews.csv")
    df["sentiment_score"] = df["review_text"].apply(analyze_sentiment)
    df.to_csv("scored_reviews.csv", index=False)
    print("✅ Sentiment analysis applied to real-time reviews.")

if __name__ == "__main__":
    score_real_time_reviews()