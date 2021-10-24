import after_response
from rest_framework import generics
from rest_framework import exceptions
from django.contrib.auth import logout
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_jwt.settings import api_settings
from user_app.utils import calculate_db_response_time
from user_app.models import Account as User, Followers
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action, permission_classes
from django.db.models import Q
from posts_app.models import Posts
from .serializers import (
    UserSerializer, SignUpSerializer,
    FollowersSerializer, FollowingsSerializer,
    UpdatePasswordSerializer
    )


@permission_classes((permissions.AllowAny,))
class UserApis(viewsets.ViewSet):  # User class
    """
    endpoints for
    signup, login, update_profile and signout
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
                'Email and Password required')
        user = User.objects.filter(email=email).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('User not Found!')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('Incorrect Password')
        serialized_user = UserSerializer(user).data
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        data = {
            'token': token,
            'user_info': serialized_user,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    # authentication requried views

    @action(detail=False, methods=['put', 'get'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user_obj = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user_obj)
        if request.method == "PUT":
            profile_data = request.data.copy()
            profile_image = request.data.get("profile_image", None)
            if profile_image == "":
                profile_data.pop("profile_image")
            serializer = UserSerializer(user_obj, data=profile_data, partial=True)
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


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = UpdatePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class UserFollowActions(viewsets.ViewSet):
    
    @action(detail=False, methods=['put'])
    def unfollow(self, request):
        """unfollow user"""
        unfollow_id = request.data.get("unfollow_id", None)
        if (unfollow_id is None):
            return Response({"msg": "unfollow to required"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Followers.objects.filter(follower=request.user, followed_id=unfollow_id, is_active=True)
        if queryset:
            queryset.update(is_active=False)
            print("im here")
            self.after_follow_action.after_response(request.user.id, unfollow_id, False)
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
        print("is_user", is_user)
        if not is_user:
            return Response({"msg": "No Such User Found"}, status=status.HTTP_404_NOT_FOUND)
        is_obj = Followers.objects.filter(follower=request.user, followed_id=follow_id).exists()
        if is_obj:
            follower_obj = Followers.objects.get(follower=request.user, followed_id=follow_id)
            if follower_obj.is_active:
                return Response({"msg": "Already Following"}, status=status.HTTP_200_OK)
            else:
                self.after_follow_action.after_response(request.user.id, follow_id, True)
                follower_obj.is_active = True
                follower_obj.save()
                msg = "Started Following {}".format(follower_obj.followed.email)
                return Response({"msg": msg}, status=status.HTTP_200_OK)
        else:
            self.after_follow_action.after_response(request.user.id, follow_id, True)
            new_obj = Followers.objects.create(follower=request.user, followed_id=follow_id)
            msg = "Started Following {}".format(new_obj.followed.email)
            return Response({"msg": msg}, status=status.HTTP_200_OK)


    @after_response.enable
    def after_follow_action(current_user_id, follow_id, is_follow):
        follow_to_user = User.objects.get(id=follow_id)
        all_posts = Posts.my_posts(follow_to_user)
        all_posts_instances = []
        ThroughModel  = Posts.show_to_users.through
        for post in all_posts:
            if is_follow:
                all_posts_instances.append(ThroughModel(account_id=current_user_id, posts_id=post.pk))
            else:
                post.show_to_users.remove(current_user_id)
        if is_follow:
            ThroughModel.objects.bulk_create(all_posts_instances, batch_size=100)


class UserFollowers(generics.ListAPIView):
    serializer_class = FollowersSerializer
    pagination_class = UserCustomPagination 

    def get_queryset(self):
        """return list of current user followers"""
        queryset = Followers.get_active_followers(self.request.user)
        return queryset


class UserFollowing(generics.ListAPIView):
    serializer_class = FollowingsSerializer
    pagination_class = UserCustomPagination 

    def get_queryset(self):
        """return list of current user followings"""
        queryset = Followers.get_active_followings(self.request.user)
        return queryset


class UsersList(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = UserCustomPagination

    def get_queryset(self):
        searched_query = self.request.query_params.get('searched_query', None)
        print("searched_query", searched_query)
        filter = Q()
        if searched_query:
            searched_query = searched_query.strip()
            if searched_query:
                filter = Q(Q(email__icontains=searched_query) | Q(username__icontains=searched_query))
        query_set = User.objects.filter(filter, is_active=True).exclude(id=self.request.user.id).extra(select={
        'is_following': 'SELECT COUNT(*) FROM user_app_followers WHERE ' +
        'follower_id=%s AND followed_id = user_app_account.id AND is_active=True'
                                },select_params=(self.request.user.id,))        
        calculate_db_response_time()
        return query_set

