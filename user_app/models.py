from PIL import Image
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from user_app.utils import get_upload_path
from user_app.managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Account(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    email_verified = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    class Meta:
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            img = Image.open(self.profile_image.path)    
            if img.height > 300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)


class Followers(models.Model):
    follower = models.ForeignKey(Account, on_delete=CASCADE, related_name="follower")
    followed = models.ForeignKey(Account, on_delete=CASCADE, related_name="followed")
    followed_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Followers'
        unique_together = (('follower', 'followed'),) 
    
    @classmethod
    def get_active_followers(cls, user):
        """return the followers of current """
        return cls.objects.filter(is_active=True, followed=user).order_by("-followed_on")

    @classmethod
    def get_active_followings(cls, user, **kwargs):
        """return the following of current user"""
        return cls.objects.filter(is_active=True, follower=user, **kwargs).order_by("-followed_on")