from django_rq import job

from src.core.models import ProcessedTweet
from src.core.noise_bot.twitter_client import NoiseBotTwitterClient
from src.core.noise_bot.bot import NoiseBot, BienalBot


def reply_to_tweet_task(processed_tweet_id):
    try:
        processed_tweet = ProcessedTweet.objects.processing().get(id=processed_tweet_id)
    except ProcessedTweet.DoesNotExist:
        return None

    bot = BienalBot()
    api_client = NoiseBotTwitterClient()

    try:
        tweet = api_client.get_tweet(processed_tweet.related_tweet_id)
        reply = api_client.reply_tweet(bot, tweet)
        processed_tweet.update_with_reply(reply)
    except Exception as e:
        ## TODO/CHECK: How to handle deleted tweets?
        processed_tweet.status = ProcessedTweet.FAILED
        processed_tweet.save()
        raise e


@job
def fetch_new_tweets_task():
    from src.core.use_cases import fetch_new_tweets_use_case
    fetch_new_tweets_use_case()


@job
def reply_to_mentions_task():
    from src.core.use_cases import reply_to_mentions_use_case
    reply_to_mentions_use_case()


@job
def reply_to_hashtag_task():
    from src.core.use_cases import reply_to_hashtag_use_case
    reply_to_hashtag_use_case()
