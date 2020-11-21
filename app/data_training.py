# Load the model
import pandas as pd
import tweepy
import numpy as np 
import psycopg2
# from tensorflow import keras
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

# Twitter API Keys
consumer_key = 'q'
consumer_secret= 'V'
access_token= '1'
access_token_secret=''

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

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
        host="dacom",
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("""SELECT * FROM tweet_wordcloud""")
    rows = cur.fetchall()
    tweetcloudPd = pd.DataFrame(rows)
    tweetcloudPd.columns = ["tag", "count", "name"]
    return tweetcloudPd

def  get_wordcloud(tweetcloudPd, name):
    wordCloud = []
    for row in tweetcloudPd[tweetcloudPd['name']== name].iterrows():
        wordCloud.append({
            'tag': row[1]['tag'],
            'count': row[1]['count']
        })

    return wordCloud


def get_attitude(model_sentiment,tokenizer, tweets):

    print("========================================")

    tokens = tokenizer.texts_to_sequences(tweets)
    tokens_pad = pad_sequences(tokens, maxlen=544,
                               padding='pre', truncating='pre')

    result = model_sentiment.predict(tokens_pad)
    print("========================================", np.mean(result))
    return (float(np.mean(result)), result)


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

def retrieve_current_tweet(target_user):
    
    
    cleanContent = []
    counter = 0 
    while len(cleanContent)<20:
        public_tweets = api.user_timeline(id = target_user, page = 1 + counter )
        for tweet in public_tweets:
            if tweet["text"].find("RT")>=0:
                print("out-------------------")
                continue

            content = tweet["text"].split('…')[0].split('https://')[0]
            at = content.find("@")
            while at>=0:
                space = content[at:].find(" ")
                if space < 0:
                    space = content[at:].find(",")
                if space >=0:
                    content = content[:at] + content[at + space:]
                else:
                    content = content[:at]
                at = content.find("@")

            if len(content)> 26:
                cleanContent.append(content)
                if len(cleanContent) >=20:
                    break


    return cleanContent
