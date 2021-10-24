from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Posts
from user_app.models import Followers


@receiver(post_save, sender=Posts)
def update_post_users(sender, instance, *args, **kwargs):
    """add users to post show_to_users field"""
    followers = Followers.get_active_followers(instance.user).values_list("follower_id", flat=True)
    instance.show_to_users.set(list(followers))

        