from tweepy import Cursor

from src.core.noise_bot.twitter_api import get_api_connection


class NoiseBotTwitterClient:
    OFFICIAL_HASHTAG = '#33bienal'
    TWITTER_ACCOUNT = 'outra33bienal'

    def __init__(self, bot):
        self.api = get_api_connection()
        self.bot = bot

    def _extract_id_and_username(self, tweet):
        tweet_id = tweet.user.id
        username = tweet.user.screen_name
        return tweet_id, username

    def _search_tweets(self, search, since_id=None):
        kwargs = {}
        if since_id:
            kwargs['since_id'] = since_id
        return Cursor(self.api.search, search, **kwargs).items()

    def new_random_tweet(self):
        text = self.bot.speak_random_line()
        return self.api.update_status(text)

    def reply_tweet(self, tweet):
        tweet_id, username = self._extract_id_and_username(tweet)
        text = self.bot.reply_to(tweet.text)
        tweet_msg = "@{} {}".format(username, text)
        return self.api.update_status(tweet_msg, in_reply_to_status_id=tweet_id)

    def tweets_with_official_hashtag(self, since_id=None):
        return self._search_tweets(self.OFFICIAL_HASHTAG, since_id)

    def mentions(self, since_id=None):
        search = '@{}'.format(self.TWITTER_ACCOUNT)
        return self._search_tweets(search, since_id)
