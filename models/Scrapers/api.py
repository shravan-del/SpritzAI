from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/recommendations/")
def get_recommendations():
    df = pd.read_csv("personalized_recommendations.csv")
    return df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)