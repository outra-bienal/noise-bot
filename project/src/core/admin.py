from django.contrib import admin
from django.utils.html import format_html

from src.core.models import ProcessedTweet


class ProcessedTweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'tweet', 'created_at', 'status', 'type', 'published_tweet']
    readonly_fields = ['related_tweet_id', 'published_tweet_id', 'created_at', 'updated_at', 'status', 'type', 'reply_job_id', 'username']
    list_filter = ['status', 'type']

    def has_add_permission(self, request):
        return False

    def tweet(self, obj):
        url = 'https://twitter.com/{}/status/{}'.format(obj.username, obj.related_tweet_id)
        return format_html("<a href='{url}' target='_blank'>{url}</a>", url=url)
    tweet.short_description = "Tweet de Resposta"

    def published_tweet(self, obj):
        if not obj.published_tweet_id:
            return ''
        url = 'https://twitter.com/outra33bienal/status/{}'.format(obj.published_tweet_id)
        return format_html("<a href='{url}' target='_blank'>{url}</a>", url=url)
    published_tweet.short_description = "Tweet de Resposta"


admin.site.register(ProcessedTweet, ProcessedTweetAdmin)
