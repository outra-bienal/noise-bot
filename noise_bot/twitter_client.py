from noise_bot.twitter_api import twitter_api


class NoiseBotTwitterClient:

    def __init__(self, bot):
        self.api = twitter_api
        self.bot = bot

    def _extract_id_and_username(self, tweet):
        tweet_id = tweet.user.id
        username = tweet.user.screen_name
        return tweet_id, username

    def new_random_tweet(self):
        text = self.bot.speak_random_line()
        self.api.update_status(text)

    def reply_tweet(self, tweet):
        tweet_id, username = self._extract_id_and_username(tweet)
        text = self.bot.reply_to(tweet.text)
        tweet_msg = "@{} {}".format(username, text)
        self.api.update_status(tweet_msg, in_reply_to_status_id=tweet_id)
