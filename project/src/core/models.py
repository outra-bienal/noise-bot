from django.db import models


class ProcessedTweetQuerySet(models.QuerySet):

    def most_recent(self):
        try:
            return self.first()
        except self.model.DoesNotExist:
            return None

    def new(self):
        return self.filter(status=self.model.NEW)

    def processed(self):
        return self.exclude(published_tweet_id='')

    def processing(self):
        return self.filter(status=self.model.PROCESSING)

    def mentions(self):
        return self.filter(type=self.model.MENTION)

    def hashtags(self):
        return self.filter(type=self.model.HASHTAG)


class ProcessedTweet(models.Model):
    NEW, PROCESSING, PUBLISHED, FAILED = 1, 2, 3, 4
    MENTION, HASHTAG = 1, 2
    STATUS = (
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (PUBLISHED, 'Published'),
        (FAILED, 'Failed'),
    )
    TYPES = (
        (MENTION, 'Mention'),
        (HASHTAG, 'Hashtag Reply'),
    )

    objects = ProcessedTweetQuerySet.as_manager()

    username = models.CharField(max_length=100, default='')
    related_tweet_id = models.CharField(max_length=100, unique=True, db_index=True)
    published_tweet_id = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(choices=STATUS, default=NEW)
    type = models.SmallIntegerField(choices=TYPES)
    reply_job_id = models.CharField(max_length=100, default='')
    error_message = models.TextField(default='')

    class Meta:
        ordering = ['-created_at']

    def update_with_reply(self, reply):
        ## TODO/CHECK: É assim mesmo que se recupera o ID de um Status (Tweet)?
        self.published_tweet_id = reply.id
        self.status = self.PUBLISHED
        self.save()
