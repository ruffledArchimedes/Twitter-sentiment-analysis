import pandas as pd
import re
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Download stopwords if not present
import nltk
nltk.download('stopwords')

# Load data
col_names = ['target', 'id', 'date', 'flag', 'user', 'text']
dataset = pd.read_csv('training.1600000.processed.noemoticon.csv', encoding='ISO-8859-1')
dataset = dataset.head(10000)  # Use only the first 10,000 rows for faster testing
dataset.columns = col_names

dataset['target'] = dataset['target'].map({4:1, 0:0})

# Stemming function
def stemming(content):
    stremmer = PorterStemmer()
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [stremmer.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

dataset['text'] = dataset['text'].apply(stemming)

x = dataset['text']
y = dataset['target']

# Split data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Vectorize
vectorizer = TfidfVectorizer()
x_train = vectorizer.fit_transform(x_train)

# Train model
model = LogisticRegression(max_iter=200)
model.fit(x_train, y_train)

# Save model and vectorizer
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))

print('model.pkl and vectorizer.pkl have been created.') 