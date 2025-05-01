# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords')"

# Create a health check script
RUN echo '#!/bin/bash\ncurl -f http://localhost:8502/healthz || exit 1' > /healthcheck.sh && \
    chmod +x /healthcheck.sh

# Expose the port Streamlit runs on
EXPOSE 8502

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD /healthcheck.sh

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]