from django.contrib import admin

from src.core.models import ProcessedTweet


class ProcessedTweetAdmin(admin.ModelAdmin):
    list_display = ['related_tweet_id', 'created_at', 'status', 'type', 'published_tweet_id']
    readonly_fields = ['related_tweet_id', 'published_tweet_id', 'created_at', 'updated_at', 'status', 'type', 'reply_job_id']
    list_filter = ['status', 'type']

    def has_add_permission(self, request):
        return False


admin.site.register(ProcessedTweet, ProcessedTweetAdmin)
