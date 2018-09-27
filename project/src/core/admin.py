from django.contrib import admin
from django.utils.html import format_html

from src.core.models import ProcessedTweet


class ProcessedTweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'type', 'username_link', 'tweet', 'created_at', 'published_tweet']
    readonly_fields = ['related_tweet_id', 'published_tweet_id', 'created_at', 'updated_at', 'type', 'reply_job_id', 'username', 'error_message']
    list_filter = ['status', 'type', 'created_at']
    search_fields = ['username']
    actions = ['mark_as_new']

    def has_add_permission(self, request):
        return False

    def tweet(self, obj):
        url = 'https://twitter.com/{}/status/{}'.format(obj.username, obj.related_tweet_id)
        return format_html("<a href='{url}' target='_blank'>Link</a>", url=url)
    tweet.short_description = "Tweet Original"

    def username_link(self, obj):
        url = 'https://twitter.com/{}/'.format(obj.username)
        return format_html("<a href='{url}' target='_blank'>{user}</a>", url=url, user=obj.username)
    tweet.short_description = "Tweet Original"

    def published_tweet(self, obj):
        if obj.error_message:
            return format_html('<pre><code>{msg}</code></pre>', msg=obj.error_message)
        if not obj.published_tweet_id:
            return ''
        url = 'https://twitter.com/outra33bienal/status/{}'.format(obj.published_tweet_id)
        return format_html("<a href='{url}' target='_blank'>Link</a>", url=url)
    published_tweet.short_description = "Resposta"

    def mark_as_new(modeladmin, request, queryset):
        queryset.update(status=ProcessedTweet.NEW)


admin.site.register(ProcessedTweet, ProcessedTweetAdmin)
