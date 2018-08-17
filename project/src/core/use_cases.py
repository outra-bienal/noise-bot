from src.core.models import ProcessedTweet
from src.core.noise_bot.twitter_client import NoiseBotTwitterClient
from src.core.noise_bot.utils import extract_id_and_username


def fetch_new_tweets_use_case():
    print('Fetching new tweets...')

    api_client = NoiseBotTwitterClient()
    kwargs = {}

    most_recent = ProcessedTweet.objects.most_recent()
    if most_recent:
        kwargs['since_id'] = most_recent.related_tweet_id

    tweets = api_client.mentions(**kwargs)
    for i, tweet in enumerate(tweets):
        tweet_id, username = extract_id_and_username(tweet)
        ProcessedTweet.objects.get_or_create(
            related_tweet_id=tweet_id,
            defaults={'type': ProcessedTweet.MENTION},
        )
    print('\t{} new mentions'.format(i + 1))

    tweets = api_client.tweets_with_official_hashtag(**kwargs)
    for i, tweet in enumerate(tweets):
        tweet_id, username = extract_id_and_username(tweet)
        ProcessedTweet.objects.get_or_create(
            related_tweet_id=tweet_id,
            defaults={'type': ProcessedTweet.HASHTAG},
        )
    print('\t{} new tweets with official hashtag'.format(i + 1))
