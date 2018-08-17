def extract_id_and_username(tweet):
    ## TODO/CHECK: É assim mesmo que se recupera o ID de um Status (Tweet)?
    ## TODO/CHECK: esse ID não é o ID do usuário ao invés do ID do tweet?
    ## Parece que não: https://stackoverflow.com/questions/10804507/how-to-get-tweet-ids-since-id-max-id-in-tweepy-python
    tweet_id = tweet.user.id
    username = tweet.user.screen_name
    return tweet_id, username
