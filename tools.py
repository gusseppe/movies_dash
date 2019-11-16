import re
import glob
import nltk
import config
import os

import tweepy
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tweepy import OAuthHandler
from textblob import TextBlob


def remove_local_files():
    path = f"{os.path.join('local', '*.json')}"
    for fl in glob.glob(path):
        print(f'Removing file: {fl}')
        os.remove(fl)


def drop_mongo():
    from pymongo import MongoClient # Libreria que se conecta al mongodb. Instalar mongodb previamente.
    client = MongoClient('localhost', 27017)

    db = client.test_database # El nomnbre de la base de datos, en este caso,  peliculas
    collections = db.list_collection_names()
    for c in collections:
        print(f'Removing collection: {c}')
        db[c].drop()

class TwitterClient(object):
    '''
	Based on: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

	'''

    def __init__(self):
        '''
            Clase que se encarga de conectarse a la API de Twitter
		'''
        # Credenciales de Twitter
        # Las dos primeras identifican que aplicacion de twitter vas a usar.
        consumer_key = config.consumer_key
        consumer_secret = config.consumer_secret
        # Las credenciales del API (para acceder) de esa aplicacion.
        access_token = config.access_token
        access_token_secret = config.access_token_secret

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)

            # Llama a la libreria tweepy para ingresar las credenciales y obtener un objecto api.
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Ha fallado la autentificacion")

    def clean_tweet(self, tweet):
        '''
            Se encarga de limpias los tweets, o sea, las revies de las peliculas.
            Le quita los valores no alfanumericos, p.e, guion, slash, arrobas etc.
		'''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # self.filter_tweet = ' '.join(re.sub('[^a-zA-Z ]', "", tweet).split())
    # return self.filter_tweet

    def get_tweet_sentiment(self, tweet):
        '''

		'''
        # Crea el objeto que se encarga de obtener el sentimiento, polaridad de los tweets.
        text_obj = TextBlob(self.clean_tweet(tweet))
        try:
            text_translated = text_obj.translate(from_lang='es', to='en')
        except:
            text_translated = self.clean_tweet(tweet)

        analysis = TextBlob(str(text_translated))
        # sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
            Se encarga de conectar a twitter.
		'''
        # empty list to store parsed tweets
        tweets = []

        try:
            # Busca los tweets correspondientes al query, p.e, joker, en espanol. search hace eso.
            fetched_tweets = self.api.search(q=query, count=count, lang='es')

            for tweet in fetched_tweets:
                parsed_tweet = {}

                # Guardamos cada tweet en un diccionario
                parsed_tweet['name'] = query
                parsed_tweet['text_original'] = tweet.text
                parsed_tweet['text_cleaned'] = self.clean_tweet(tweet.text)
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # Si tiene retweets, solo coge un solo tweet.
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print('La conexion ha fallado.')
