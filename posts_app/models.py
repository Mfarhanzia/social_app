from django.db import models
from django.db.models import Q 
from user_app.models import Account
from posts_app.utils import get_post_file_upload_path

# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(Account, related_name="user", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    detail = models.TextField(blank=True, null=True)
    post_image = models.ImageField(upload_to=get_post_file_upload_path, blank=True, null=True)
    show_to_users = models.ManyToManyField(Account)  #show private posts to these
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email)

    @classmethod
    def active_records(cls):
        return cls.objects.filter(is_deleted=False).order_by("-created_at")

    @classmethod
    def get_public_posts(cls):
        return cls.objects.filter(is_public=True, is_deleted=False).order_by("-created_at")
    
    @classmethod
    def my_posts(cls, user):
        return cls.objects.filter(is_deleted=False, user=user).order_by("-created_at")
    
    @classmethod
    def get_feeds(cls, user):
        return cls.objects.filter(Q(is_public=True) | Q(show_to_users=user) | Q(user=user), is_deleted=False).order_by("-created_at")
    
    class Meta:
        verbose_name_plural = 'Posts'


# class NewsFeeds(models.Model):
#     post_obj = models.ForeignKey(Posts, on_delete=models.CASCADE)
#     users = models.ManyToManyField(Account)
#     is_public = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)
