from tweepy import OAuthHandler, API
from unittest.mock import patch, Mock
from decouple import config

from noise_bot.twitter_api import get_api_connection

CONSUMER_KEY = config('TWITTER_APP_CONSUMER_KEY')
CONSUMER_SECRET = config('TWITTER_APP_CONSUMER_SECRET')
ACCESS_TOKEN = config('TWITTER_APP_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('TWITTER_APP_ACCESS_TOKEN_SECRET')


@patch('noise_bot.twitter_api.tweepy')
def test_api_connection(mocked_tweepy):
    auth = mocked_tweepy.OAuthHandler.return_value
    api = mocked_tweepy.API.return_value

    get_api_connection._conn = None
    api_conn = get_api_connection()

    assert api == api_conn
    assert api == get_api_connection._conn
    mocked_tweepy.OAuthHandler.assert_called_once_with(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token.assert_called_once_with(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    mocked_tweepy.API.assert_called_once_with(auth)
