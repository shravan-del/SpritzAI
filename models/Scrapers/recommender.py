import pandas as pd

user_preferences = {
    "preferred_sentiment": 4,  
    "min_rating": 3.5, 
}

df = pd.read_csv("scored_reviews.csv")

def personalized_recommendations():
    recommendations = df[
        (df["sentiment_score"] >= user_preferences["preferred_sentiment"]) &
        (df["rating"] >= user_preferences["min_rating"])
    ]
    
    recommendations.to_csv("personalized_recommendations.csv", index=False)
    print("Updated personalized recommendations.")

if __name__ == "__main__":
    personalized_recommendations()