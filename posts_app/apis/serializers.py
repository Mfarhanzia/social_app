from django.db import models
from django.db.models.expressions import OrderBy
from rest_framework import serializers
from posts_app.models import Posts
from user_app.models import Account
from user_app.apis.serializers import UserSerializer 


class PostsSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=False)
    
    class Meta:
        model = Posts
        fields = ("id", "user", "title", "detail", "post_image", "is_public", "created_at")
        
        extra_kwargs = {
            "created_at": {"read_only": True}
        }

class PostsUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    
    class Meta:
        model = Posts
        fields = ("id", "user", "title", "detail", "post_image", "is_public", "created_at")
        
        extra_kwargs = {
            "created_at": {"read_only": True}
        }