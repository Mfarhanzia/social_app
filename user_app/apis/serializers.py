from rest_framework import serializers
from user_app.models import Account


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
    
    class Meta:
        model = Account
        fields = ("profile_image", "username", "email", "first_name", "last_name", "date_joined", "is_active") 

        extra_kwargs = {
            "date_joined": {"read_only": True},
            "is_active": {"read_only": True},
        }       