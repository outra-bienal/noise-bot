from tweepy import Cursor

from src.core.noise_bot.twitter_api import get_api_connection
from src.core.noise_bot.utils import extract_id_and_username


def clean_text(text):
    invalid_word = lambda w: w.startswith('#') or w.startswith('@')
    return ' '.join([w for w in text.split(' ') if not invalid_word(w)])


class NoiseBotTwitterClient:
    OFFICIAL_HASHTAGS = [
        '#33bienal',
        '#afinidadesafetivas',
        '#bienalsaopaulo',
        '#bienalsp',
        '#bienal2018',
        '#bienaldesaopaulo'
    ]

    def __init__(self):
        self.api = get_api_connection()
        self.username = '@outra33bienal'

    def _search_tweets(self, search, since_id=None):
        kwargs = {}
        if since_id:
            kwargs['since_id'] = since_id
        return Cursor(self.api.search, search, **kwargs).items()

    def new_random_tweet(self, bot):
        text = bot.speak_random_line()
        return self.api.update_status(text)

    def reply_tweet(self, bot, tweet):
        tweet_id, username = extract_id_and_username(tweet)
        photos = [m for m in tweet.entities.get('media', []) if m.get('type') == 'photo']

        kwargs = {}
        if photos and self.username in tweet.text:
            glitch = bot.glitch_image(photos[0]['media_url'])
            upload = self.api.media_upload(glitch.name, in_reply_to_status_id=tweet_id, file=glitch)
            tweet_msg = '@{}'.format(username)
            kwargs['media_ids'] = [upload.media_id]
        else:
            text = bot.reply_to(clean_text(tweet.text))
            tweet_msg = "@{} {}".format(username, text)

        return self.api.update_status(tweet_msg, in_reply_to_status_id=tweet_id, **kwargs)

    def tweets_with_official_hashtag(self, since_id=None):
        q = ' OR '.join(self.OFFICIAL_HASHTAGS)
        for tweet in self._search_tweets(q, since_id):
            yield tweet

    def mentions(self, since_id=None):
        return self.api.mentions_timeline()

    def get_tweet(self, tweet_id):
        return self.api.get_status(tweet_id)
