def extract_id_and_username(tweet):
    tweet_id = tweet.id
    username = tweet.user.screen_name
    return tweet_id, username
