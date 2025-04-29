import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import tweepy
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Download stopwords once, using Streamlit's caching
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')

# Initialize the vectorizer
@st.cache_resource
def initialize_vectorizer():
    return TfidfVectorizer()

# Load model and vectorizer once
@st.cache_resource
def load_model_and_vectorizer():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

# Initialize stemmer
@st.cache_resource
def initialize_stemmer():
    return PorterStemmer()

# Function to preprocess text
def preprocess_text(text):
    # Initialize stemmer
    stemmer = initialize_stemmer()
    
    # Remove special characters and convert to lowercase
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    
    # Split into words, stem, and remove stopwords
    text = text.split()
    text = [stemmer.stem(word) for word in text if not word in stopwords.words('english')]
    text = ' '.join(text)
    return text

# Function to predict sentiment
def predict_sentiment(text, model, vectorizer):
    processed_text = preprocess_text(text)
    text_vector = vectorizer.transform([processed_text])
    sentiment = model.predict(text_vector)[0]
    confidence = model.predict_proba(text_vector)[0]
    return "Positive" if sentiment == 1 else "Negative", max(confidence)

# Function to create a colored card
def create_card(tweet_text, sentiment, confidence, date=None, username=None):
    color = "#4CAF50" if sentiment == "Positive" else "#f44336"
    emoji = "😊" if sentiment == "Positive" else "😞"
    confidence_percent = f"{confidence*100:.1f}%"
    
    card_html = f"""
    <div style="background-color: {color}; padding: 15px; border-radius: 10px; margin: 10px 0; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0;">{emoji} {sentiment} Sentiment</h4>
            <span style="background-color: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px;">
                Confidence: {confidence_percent}
            </span>
        </div>
        {f'<p style="margin: 5px 0; font-size: 0.9em;">@{username} • {date}</p>' if username and date else ''}
        <p style="margin: 10px 0;">{tweet_text}</p>
    </div>
    """
    return card_html

# Function to fetch tweets using Twitter API with rate limit handling
def fetch_tweets(username, limit=10):
    try:
        # Initialize Twitter client
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True  # This will automatically handle rate limits
        )
        
        # Get user ID
        user = client.get_user(username=username)
        if not user.data:
            return None
            
        # Fetch tweets with pagination
        tweets = []
        for tweet in tweepy.Paginator(
            client.get_users_tweets,
            user.data.id,
            max_results=min(limit, 100),  # Twitter API has a max of 100 per request
            tweet_fields=['created_at'],
            limit=limit
        ):
            if tweet.data:
                for t in tweet.data:
                    tweets.append({
                        'content': t.text,
                        'date': t.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'username': username
                    })
                    if len(tweets) >= limit:
                        break
            if len(tweets) >= limit:
                break
                
        return tweets[:limit]  # Ensure we don't return more than requested
        
    except tweepy.TooManyRequests:
        st.error("Rate limit exceeded. Please wait a few minutes and try again.")
        return None
    except tweepy.Unauthorized:
        st.error("Invalid Twitter API credentials. Please check your credentials.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Twitter Sentiment Analysis", page_icon="📊")
    
    st.title("📊 Twitter Sentiment Analysis")
    st.markdown("""
    This app analyzes the sentiment of tweets. You can:
    - Fetch and analyze tweets from any Twitter user
    - Analyze your own text
    - Try example tweets
    """)
    
    # Load required components
    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()
    stemmer = initialize_stemmer()
    
    # Twitter API credentials section
    st.sidebar.subheader("Twitter API Credentials")
    api_key = st.sidebar.text_input("API Key", type="password")
    api_secret = st.sidebar.text_input("API Secret", type="password")
    bearer_token = st.sidebar.text_input("Bearer Token", type="password")
    access_token = st.sidebar.text_input("Access Token", type="password")
    access_token_secret = st.sidebar.text_input("Access Token Secret", type="password")
    
    # Save credentials to environment variables
    if all([api_key, api_secret, bearer_token, access_token, access_token_secret]):
        os.environ['TWITTER_API_KEY'] = api_key
        os.environ['TWITTER_API_SECRET'] = api_secret
        os.environ['TWITTER_BEARER_TOKEN'] = bearer_token
        os.environ['TWITTER_ACCESS_TOKEN'] = access_token
        os.environ['TWITTER_ACCESS_TOKEN_SECRET'] = access_token_secret
    
    # Twitter search section
    st.subheader("🔍 Fetch Tweets from Twitter")
    username = st.text_input("Enter Twitter username (without @)")
    tweet_limit = st.slider("Number of tweets to fetch", 1, 50, 10)
    
    if st.button("Fetch and Analyze Tweets"):
        if not all([api_key, api_secret, bearer_token, access_token, access_token_secret]):
            st.error("Please enter all Twitter API credentials in the sidebar")
            return
            
        if username.strip():
            with st.spinner("Fetching tweets..."):
                tweets = fetch_tweets(username, tweet_limit)
                if tweets:
                    st.success(f"Found {len(tweets)} tweets!")
                    for tweet in tweets:
                        sentiment, confidence = predict_sentiment(tweet['content'], model, vectorizer)
                        st.markdown(create_card(
                            tweet['content'],
                            sentiment,
                            confidence,
                            tweet['date'],
                            tweet['username']
                        ), unsafe_allow_html=True)
                else:
                    st.warning("No tweets found for this user.")
        else:
            st.warning("Please enter a Twitter username.")
    
    # Single text analysis section
    st.subheader("📝 Analyze Your Text")
    text_input = st.text_area("Enter your text here:", height=100)
    
    if st.button("Analyze Sentiment"):
        if text_input.strip():
            sentiment, confidence = predict_sentiment(text_input, model, vectorizer)
            st.markdown(create_card(text_input, sentiment, confidence), unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to analyze.")
    
    # Example tweets section
    st.subheader("💡 Try Example Tweets")
    example_tweets = [
        "I love this product! It's amazing and works perfectly!",
        "The service was terrible. I'm never coming back here again.",
        "Just had the best meal of my life at this restaurant!",
        "Worst customer service experience ever. Avoid at all costs.",
        "The movie was absolutely fantastic! Must watch!"
    ]
    
    cols = st.columns(5)
    for i, tweet in enumerate(example_tweets):
        if cols[i % 5].button(tweet[:30] + "..." if len(tweet) > 30 else tweet, key=f"example_{i}"):
            sentiment, confidence = predict_sentiment(tweet, model, vectorizer)
            st.markdown(create_card(tweet, sentiment, confidence), unsafe_allow_html=True)

if __name__ == "__main__":
    main()