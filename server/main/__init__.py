import os
from flask import Flask, request, jsonify
import tweepy

# utilities
import re
import pickle
import numpy as np

# nltk
from nltk.stem import WordNetLemmatizer

# sklearn
from sklearn.naive_bayes import BernoulliNB

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report

# --------------------------------------
# BASIC APP SETUP
# --------------------------------------
app = Flask(__name__, instance_relative_config=True)

# Config
app_settings = os.getenv(
    'APP_SETTINGS',
    'main.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Extensions
from flask_cors import CORS
CORS(app)

# Load Model
model = pickle.load(open('main/Sentiment-BNB.pickle', 'rb'))

# Twitter
auth = tweepy.OAuthHandler(app.config.get('CONSUMER_KEY'), app.config.get('CONSUMER_SECRET'))
auth.set_access_token(app.config.get('ACCESS_TOKEN'), app.config.get('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth,wait_on_rate_limit=True)

# loading vectorizer
with open('main/vectorizer-ngram-(1,2).pickle', 'rb') as handle:
    vectorizer = pickle.load(handle)

def preprocess(textdata):
    processedText = []
    
    # Create Lemmatizer and Stemmer.
    wordLemm = WordNetLemmatizer()
    
    # Defining regex patterns.
    urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern       = '@[^\s]+'
    alphaPattern      = "[^a-zA-Z0-9]"
    sequencePattern   = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"
    
    for tweet in textdata:
        tweet = tweet.lower()
        
        # Replace all URls with 'URL'
        tweet = re.sub(urlPattern,' URL',tweet)
        
        # Replace all emojis.
        for emoji in emojis.keys():
            tweet = tweet.replace(emoji, "EMOJI" + emojis[emoji])
            
        # Replace @USERNAME to 'USER'.
        tweet = re.sub(userPattern,' USER', tweet)
        
        # Replace all non alphabets.
        tweet = re.sub(alphaPattern, " ", tweet)
        
        # Replace 3 or more consecutive letters by 2 letter.
        tweet = re.sub(sequencePattern, seqReplacePattern, tweet)

        tweetwords = ''
        for word in tweet.split():
            # Checking if the word is a stopword.
            #if word not in stopwordlist:
            if len(word)>1:
                # Lemmatizing the word.
                word = wordLemm.lemmatize(word)
                tweetwords += (word+' ')
            
        processedText.append(tweetwords)
        
    return processedText

def predict(text, include_neutral=True):

    # Vectorizer
    textdata = vectorizer.transform(preprocess(text))

    # Predict
    pos, neg = model.predict_proba(textdata)[0]

    if(pos >= 0.4 and pos <=0.6):
        label = "Neutral"
    if(pos <=0.4):
        label = "Negative"
    if(pos >=0.6):
        label = "Positive"

    return {"label" : label,
        "score": float(pos)} 

@app.route('/')
def index():
    return 'Hello'

@app.route('/getsentiment', methods=['GET'])
def getsentiment():
    data = {"success": False}
    # if parameters are found, echo the msg parameter 
    if (request.args != None):  
        with graph.as_default():
            data["predictions"] = predict([request.args.get("text")])
        data["success"] = True
    return jsonify(data)

@app.route('/analyzehashtag', methods=['GET'])
def analyzehashtag():
    positive = 0
    neutral = 0
    negative = 0
    for tweet in tweepy.Cursor(api.search,q="#" + request.args.get("text") + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended').items(100):
        with graph.as_default():
            prediction = predict(tweet.full_text)
        if(prediction["label"] == "Positive"):
            positive += 1
        if(prediction["label"] == "Neutral"):
            neutral += 1
        if(prediction["label"] == "Negative"):
            negative += 1
    return jsonify({"positive": positive, "neutral": neutral, "negative": negative});

@app.route('/gettweets', methods=['GET'])
def gettweets():
    tweets = []
    for tweet in tweepy.Cursor(api.search,q=request.args.get("text") + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended').items(10):
        temp = {}
        temp["text"] = tweet.full_text
        temp["username"] = tweet.user.screen_name
        with graph.as_default():
            prediction = predict(tweet.full_text)
        temp["label"] = prediction["label"]
        temp["pos"] = prediction["pos"]
        tweets.append(temp)
    return jsonify({"results": tweets});
    