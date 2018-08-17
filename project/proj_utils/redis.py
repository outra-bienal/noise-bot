import django_rq
from django.conf import settings


class RedisAsyncClient(object):

    @property
    def reply_queue(self):
        return django_rq.get_queue(settings.REPLY_QUEUE)

    def enqueue_reply(self, callable, *args, **kwargs):
        if settings.TESTING:
            callable(*args, **kwargs)
            return True
        else:
            return self.reply_queue.enqueue(
                callable, args=args, kwargs=kwargs
            )


class NullableClient(object):
    """
    https://robots.thoughtbot.com/rails-refactoring-example-introduce-null-object
    """

    def enqueue_default(self, callable, *args, **kwargs):
        return callable(*args, **kwargs)
