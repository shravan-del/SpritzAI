# Use lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy script files
COPY scraper.py preprocess.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p /app/data

# Default command: run scraper
CMD ["python", "scraper.py"]