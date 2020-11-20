# Load the model
import pandas as pd
import numpy as np 
import psycopg2
# from tensorflow import keras
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# analyzer = SentimentIntensityAnalyzer()

import tensorflow as tf

def initial_model():

    # model = tf.keras.models.load_model('model/politics_model_trained.h5')
    model_biden_trump = tf.keras.models.load_model('model/model1119.h5')
    model_sentiment = tf.keras.models.load_model('model/sentimentmode.h5')

    politics_tweet_df = pd.read_csv('data/politics_tweet.csv')

    num_words = 10000
    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(politics_tweet_df["tweet"].tolist())
    
    return (model_biden_trump, model_sentiment, tokenizer)

def load_db():
    conn = psycopg2.connect(
        database="example",
        user="postgres",
        password="",
        host="",
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("""SELECT * FROM tweet""")
    rows = cur.fetchall()
    tweetPd = pd.DataFrame(rows)
    return tweetPd

def get_attitude(model_sentiment,tokenizer, tweetPd, name):

    print("========================================")
    searchTweetPd =  tweetPd[tweetPd[1]== name]
    # The computer run slow when it count entire dataset. So I have to load 10 sample data
    searchTweetPd10record = searchTweetPd.sample(n=10,replace=False) 
    
    tweetText = []
    for i in range(len(searchTweetPd10record)):
        tweetText.append(searchTweetPd10record.iloc[i,2])

    tokens = tokenizer.texts_to_sequences(tweetText)
    tokens_pad = pad_sequences(tokens, maxlen=544,
                               padding='pre', truncating='pre')

    result = model_sentiment.predict(tokens_pad)
    print("========================================", np.mean(result))
    return float(np.mean(result))


def predict(model, tokenizer,text):
    texts = [text]
    for i in range(len(texts)):
        texts[i] = texts[i].lower()
    tokens = tokenizer.texts_to_sequences(texts)
    tokens_pad = pad_sequences(tokens, maxlen=57,
                               padding='pre', truncating='pre')
    # tokens_pad.shape
    result = model.predict(tokens_pad)
    return result
