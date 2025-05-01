import pytest
from app import analyze_sentiment

def test_analyze_sentiment():
    # Test positive sentiment
    result = analyze_sentiment("I love this product! It's amazing!")
    assert result['sentiment'] == 'positive'
    
    # Test negative sentiment
    result = analyze_sentiment("This is terrible, I hate it!")
    assert result['sentiment'] == 'negative'
    
    # Test neutral sentiment
    result = analyze_sentiment("This is a regular tweet.")
    assert result['sentiment'] == 'neutral' 