# Twitter Sentiment Analysis App

A Streamlit web application that analyzes the sentiment of tweets using machine learning.

## Features

- Fetch and analyze tweets from any Twitter user
- Analyze custom text for sentiment
- Try example tweets
- Docker support for easy deployment

## Prerequisites

- Python 3.12 or higher
- Twitter API credentials (for tweet fetching feature)
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/twitter-sentiment-analysis.git
cd twitter-sentiment-analysis
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your Twitter API credentials:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

## Running the Application

### Local Development

```bash
streamlit run app.py
```

The application will be available at http://localhost:8502

### Docker

1. Build the Docker image:
```bash
docker build -t twitter-sentiment-analysis .
```

2. Run the container:
```bash
docker run -p 8502:8502 twitter-sentiment-analysis
```

The application will be available at http://localhost:8502

## Usage

1. Open the application in your web browser
2. Enter your Twitter API credentials in the sidebar
3. Choose one of the following options:
   - Fetch and analyze tweets from a Twitter user
   - Analyze your own text
   - Try example tweets

## Model Details

The sentiment analysis model is trained on a dataset of 1.6 million tweets and uses:
- TF-IDF vectorization
- Logistic Regression
- NLTK for text preprocessing

## License

This project is licensed under the MIT License - see the LICENSE file for details.