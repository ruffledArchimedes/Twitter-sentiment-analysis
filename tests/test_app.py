import pytest
from app import analyze_sentiment, preprocess_text

def test_preprocess_text():
    # Test basic preprocessing
    text = "Hello! This is a Test. 123"
    processed = preprocess_text(text)
    assert processed == "hello test"
    
    # Test stopword removal
    text = "This is a great day"
    processed = preprocess_text(text)
    assert "is" not in processed
    assert "a" not in processed
    assert "great" in processed
    assert "day" in processed

def test_analyze_sentiment():
    # Test positive sentiment
    text = "This is a great and wonderful day!"
    sentiment, confidence = analyze_sentiment(text)
    assert sentiment == "Positive"
    assert confidence > 0.5
    
    # Test negative sentiment
    text = "This is terrible and horrible."
    sentiment, confidence = analyze_sentiment(text)
    assert sentiment == "Negative"
    assert confidence > 0.5
    
    # Test neutral sentiment
    text = "This is a regular day."
    sentiment, confidence = analyze_sentiment(text)
    assert sentiment == "Neutral"
    assert confidence == 0.5
    
    # Test empty text
    text = ""
    sentiment, confidence = analyze_sentiment(text)
    assert sentiment == "Neutral"
    assert confidence == 0.5

def test_sentiment_confidence():
    # Test confidence calculation
    text = "good great excellent"  # 3 positive words
    sentiment, confidence = analyze_sentiment(text)
    assert sentiment == "Positive"
    assert confidence == 1.0
    
    # Test mixed sentiment
    text = "good bad terrible excellent"  # 2 positive, 2 negative
    sentiment, confidence = analyze_sentiment(text)
    assert sentiment == "Neutral"
    assert confidence == 0.5 