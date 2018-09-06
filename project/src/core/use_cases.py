from django.db import transaction

from proj_utils.redis import RedisAsyncClient
from src.core.models import ProcessedTweet
from src.core.noise_bot.twitter_client import NoiseBotTwitterClient
from src.core.noise_bot.utils import extract_id_and_username
from src.core.tasks import reply_to_tweet_task


def _process_tweets(tweets, tweet_type):
    total = 0
    for tweet in tweets:
        tweet_id, username = extract_id_and_username(tweet)
        ProcessedTweet.objects.get_or_create(
            related_tweet_id=tweet_id,
            defaults={'type': tweet_type, 'username': username},
        )
        total += 1
    return total


def fetch_new_tweets_use_case():
    print('Fetching new tweets...')

    api_client = NoiseBotTwitterClient()

    kwargs = {}
    last_processed = ProcessedTweet.objects.mentions().processed().most_recent()
    if last_processed:
        kwargs['since_id'] = last_processed.related_tweet_id

    tweets = api_client.mentions(**kwargs)
    total = _process_tweets(tweets, ProcessedTweet.MENTION)
    print('\t{} new mentions'.format(total))

    kwargs = {}
    last_processed = ProcessedTweet.objects.hashtags().processed().most_recent()
    if last_processed:
        kwargs['since_id'] = last_processed.related_tweet_id

    tweets = api_client.tweets_with_official_hashtag(**kwargs)
    total = _process_tweets(tweets, ProcessedTweet.HASHTAG)
    print('\t{} new tweets with official hashtag'.format(total))


def _enqueue_reply_task(processed_tweet):
    client = RedisAsyncClient()
    job = client.enqueue_reply(
        reply_to_tweet_task,
        processed_tweet_id=processed_tweet.id
    )

    processed_tweet.reply_job_id = str(job.id)
    processed_tweet.status = processed_tweet.PROCESSING
    processed_tweet.save()


@transaction.atomic
def reply_to_mentions_use_case():
    print('Processing new mentions...')
    qs = ProcessedTweet.objects.new().mentions().select_for_update()
    for processed_tweet in qs:
        _enqueue_reply_task(processed_tweet)
    print('{} replies to mentions were enqueued'.format(qs.count()))


@transaction.atomic
def reply_to_hashtag_use_case():
    print('Processing new tweets with official hashtag...')
    qs = ProcessedTweet.objects.new().hashtags().select_for_update()
    for processed_tweet in qs:
        _enqueue_reply_task(processed_tweet)
    print('{} replies to the official hashtag were enqueued'.format(qs.count()))
