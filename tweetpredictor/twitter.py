"""Retrieve TWeets, embeddings, and persist in the database."""
import tweepy
import basilica
from decouple import config
from .models import DB, Tweet, User

def authtwitter():
    """Authenticate to twitter API"""
    TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
            config('TWITTER_CONSUMER_SECRET'))
    TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
            config('TWITTER_ACCESS_TOKEN_SECRET'))
    return tweepy.API(TWITTER_AUTH)

def authbasilica():
    """Authenticate to basilica API"""
    return basilica.Connection(config('BASILICA_KEY'))

def getuser(user_name):
    """Fetch user information from Twitter"""
    TWITTER = authtwitter()
    return TWITTER.get_user(user_name)

def gettweets(user_name):
    """Fetch tweets for specific twitter user"""
    twitter_user = getuser(user_name)
    return twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')

def gettwitterembedding(text):
    """Fetch twitter based embedding from basilica"""
    BASILICA = authbasilica()
    return BASILICA.embed_sentence(text, model='twitter')
