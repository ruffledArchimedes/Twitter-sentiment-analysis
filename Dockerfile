# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with retries
RUN pip install --no-cache-dir --timeout=100 -r requirements.txt || \
    pip install --no-cache-dir --timeout=100 -r requirements.txt || \
    pip install --no-cache-dir --timeout=100 -r requirements.txt

# Copy the rest of the application
COPY . .

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords')"

# Expose the port Streamlit runs on
EXPOSE 8502

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]