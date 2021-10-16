from django.db import models
from user_app.models import Account
from posts_app.utils import get_post_file_upload_path

# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(Account, related_name="post_by", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    detail = models.TextField(blank=True, null=True)
    post_image = models.ImageField(upload_to=get_post_file_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email)

    @classmethod
    def active_records(cls):
        return cls.objects.filter(is_deleted=False)