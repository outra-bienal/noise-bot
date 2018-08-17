from src.core.models import ProcessedTweet
from src.core.noise_bot.twitter_client import NoiseBotTwitterClient
from src.core.noise_bot.bot import NoiseBot


def reply_to_tweet_task(processed_tweet_id):
    try:
        processed_tweet = ProcessedTweet.objects.processing().get(id=processed_tweet_id)
    except ProcessedTweet.DoesNotExist:
        return None

    bot = NoiseBot()
    api_client = NoiseBotTwitterClient()

    try:
        tweet = api_client.get_tweet(processed_tweet.related_tweet_id)
        reply = api_client.reply_tweet(bot, tweet)
        processed_tweet.update_with_reply(reply)
    except Exception as e:
        processed_tweet.status = ProcessedTweet.FAILED
        processed_tweet.save()
        raise e
