import math

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from subreddits.models import Subreddit


class Post(models.Model):
    title = models.CharField(max_length=200)
    post_text = models.CharField(max_length=1000, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def time_since_upload(self):
        diff = timezone.now() - self.created_at

        # Minutes
        if diff.days == 0 and 0 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 0:
                return 'Just now'
            elif minutes == 1:
                return '1 minute ago'
            else:
                return f'{minutes} minutes ago'

        # Hours
        elif diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return '1 hour ago'
            else:
                return f'{hours} hours ago'

        # Days
        elif 1 <= diff.days < 30:
            days = diff.days

            if days == 1:
                return '1 day ago'
            else:
                return f'{days} days ago'

        # Months
        elif 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return '1 month ago'
            else:
                return f'{months} months ago'

        # Years
        else:
            years = math.floor(diff.days / 365)

            if years == 1:
                return '1 year ago'
            else:
                return f'{years} years ago'


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class PostVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField()
