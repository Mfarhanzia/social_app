from rest_framework import serializers
from user_app.models import Account, Followers


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ("email", "username", "password", "password2",)
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords mismatch"})
        account.set_password(password)
        account.save()
        return account

        
class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Account
        fields = (
            "id", "profile_image", "username", "email", "first_name",
            "last_name", "date_joined", "is_active", "is_following"
        ) 

        extra_kwargs = {
            "date_joined": {"read_only": True},
            "is_active": {"read_only": True},
        }       


class FollowersSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = Followers
        fields = ("id", "follower", "followed", "followed_on", "updated_at", "is_active")

        extra_kwargs = {
            "followed_on": {"read_only": True},
            "updated_at": {"read_only": True},
            "is_active": {"read_only": True},
        }       

class FollowingsSerializer(serializers.ModelSerializer):
    followed = UserSerializer()

    class Meta:
        model = Followers
        fields = ("id", "follower", "followed", "followed_on", "updated_at", "is_active")

        extra_kwargs = {
            "followed_on": {"read_only": True},
            "updated_at": {"read_only": True},
            "is_active": {"read_only": True},
        }       
