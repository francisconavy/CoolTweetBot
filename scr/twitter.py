import tweepy
from conf.settings import consumer_key, consumer_secret, access_token, access_token_secret

def tweet(message):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(message)
    #print(message)