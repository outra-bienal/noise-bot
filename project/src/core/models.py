from django.db import models


class ProcessedTweet(models.Model):
    NEW, PROCESSING, PUBLISHED = 1, 2, 3
    MENTION, HASHTAG = 1, 2
    STATUS = (
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (PUBLISHED, 'Published'),
    )
    TYPES = (
        (MENTION, 'Mention'),
        (HASHTAG, 'Hashtag Reply'),
    )

    related_tweet_id = models.CharField(max_length=100, unique=True, db_index=True)
    published_tweet_id = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(choices=STATUS, default=NEW)
    type = models.SmallIntegerField(choices=TYPES)

    class Meta:
        ordering = ['-created_at']
