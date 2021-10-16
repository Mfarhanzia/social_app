from rest_framework.response import Response
from rest_framework import exceptions
from user_app.models import Account as User, Followers
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework_jwt.settings import api_settings
from django.shortcuts import get_object_or_404
from .serializers import (
    UserSerializer, SignUpSerializer,
    FollowersSerializer, FollowingsSerializer
    )


@permission_classes((permissions.AllowAny,))
class UserApis(viewsets.ViewSet):  # User class
    """
    this class includes all the basic operations related to user
    signup
    login
    update_profile
    signout
    """

    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "User Registered."
            data['email'] = account.email
            data['username'] = account.username
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'email and password required')
        user = User.objects.filter(email=email).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
        serialized_user = UserSerializer(user).data
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        data = {
            'access_token': token,
            'payload': payload,
            'user_info': serialized_user,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    # authentication requried views

    @action(detail=False, methods=['put', 'get'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user_obj = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user_obj)
        if request.method == "PUT":
            serializer = UserSerializer(user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def sign_out(self, request):
        logout(request)
        return Response({"msg":"Logged out"}, status=status.HTTP_200_OK)


class UserFollowers(viewsets.ViewSet):
    def list(self, request):
        """return list of current user followers"""
        # queryset = Followers.objects.filter(followed=request.user)
        queryset = Followers.get_active_followers(request.user)
        serializer = FollowersSerializer(queryset, many=True)
        return Response({"followers": serializer.data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def list_followings(self, request):
        """return list of current user followings"""
        queryset = Followers.get_active_followings(request.user)
        serializer = FollowingsSerializer(queryset, many=True)
        return Response({"followings": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'])
    def unfollow(self, request):
        """unfollow user"""
        unfollow_id = request.data.get("unfollow_id", None)
        if (unfollow_id is None):
            return Response({"msg": "unfollow to required"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Followers.objects.filter(follower=request.user, followed_id=unfollow_id, is_active=True)
        if queryset:
            queryset.update(is_active=False)
            return Response({"msg": "Unfollowed"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "No Such Following found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def follow(self, request):
        """follow user"""
        follow_id = request.data.get("follow_id", None)
        if (follow_id is None):
            return Response({"msg": "follow to required"}, status=status.HTTP_400_BAD_REQUEST)
        is_user = User.objects.filter(id=follow_id).exists()
        if not is_user:
            return Response({"msg": "No Such User Found"}, status=status.HTTP_404_NOT_FOUND)
        is_obj = Followers.objects.filter(follower=request.user, followed_id=follow_id).exists()
        if is_obj:
            follower_obj = Followers.objects.get(follower=request.user, followed_id=follow_id)
            if follower_obj.is_active:
                return Response({"msg": "Already Following"}, status=status.HTTP_200_OK)
            else:
                follower_obj.is_active = True
                follower_obj.save()
                msg = "Started Following {}".format(follower_obj.followed.email)
                return Response({"msg": msg}, status=status.HTTP_200_OK)
        else:
            new_obj = Followers.objects.create(follower=request.user, followed_id=follow_id)
            msg = "Started Following {}".format(new_obj.followed.email)
            return Response({"msg": "No Such Following found"}, status=status.HTTP_200_OK)


        

