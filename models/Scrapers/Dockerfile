FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py sentiment_analysis.py recommender.py /app/

RUN mkdir -p /app/data

CMD ["python", "scraper.py"]