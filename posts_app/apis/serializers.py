from rest_framework import serializers
from user_app.models import Account
from user_app.apis.serializers import UserSerializer 


class PostsSerializers(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        fields = ("user", "title", "detail", "post_image", "created_at")
        extra_kwargs = {
            "created_at": {"read_only": True}
        }

