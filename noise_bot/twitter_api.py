import tweepy
from decouple import config

CONSUMER_KEY = config('TWITTER_APP_CONSUMER_KEY')
CONSUMER_SECRET = config('TWITTER_APP_CONSUMER_SECRET')
ACCESS_TOKEN = config('TWITTER_APP_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('TWITTER_APP_ACCESS_TOKEN_SECRET')


def get_api_connection():
    if not getattr(get_api_connection, '_conn', None):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        get_api_connection._conn = api
    return get_api_connection._conn


twitter_api = get_api_connection()
