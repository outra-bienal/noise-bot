from tweepy import API

from unittest import TestCase
from unittest.mock import Mock, patch

from noise_bot.bot import NoiseBot
from noise_bot.twitter_client import NoiseBotTwitterClient


class NoiseBotTwitterClientTests(TestCase):

    @patch('noise_bot.twitter_client.get_api_connection')
    def setUp(self, mocked_get_api_connection):
        self.api = Mock(API)
        self.bot = Mock(NoiseBot)
        mocked_get_api_connection.return_value = self.api
        self.client = NoiseBotTwitterClient(self.bot)

    def test_new_random_tweet(self):
        text = 'hi!'
        self.bot.speak_random_line.return_value = text

        tweet = self.client.new_random_tweet()

        self.bot.speak_random_line.assert_called_once_with()
        self.api.update_status.assert_called_once_with(text)
        assert tweet == self.api.update_status.return_value

    def test_reply_tweet(self):
        user = Mock(id=42, screen_name='user')
        tweet = Mock(user=user, text='tweet text')
        text = 'hi!'
        self.bot.reply_to.return_value = text

        reply = self.client.reply_tweet(tweet)
        expected_text = '@user hi!'

        self.bot.reply_to.assert_called_once_with('tweet text')
        self.api.update_status.assert_called_once_with(
            expected_text, in_reply_to_status_id=42
        )
        assert reply == self.api.update_status.return_value
