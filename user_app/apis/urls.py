from django.urls import path
from django.urls.conf import include
# from rest_framework import routers
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from user_app.apis.views import (UserApis, UserFollowActions, UserFollowers, UsersList, ChangePasswordView,
    UserFollowing)


router = routers.DefaultRouter()
router.register(r'', UserApis, basename='user')  #User apis
router.register(r'follower', UserFollowActions, basename='followers')  #User apis

urlpatterns = [
    path('', include(router.urls)),
    path('search', UsersList.as_view()),
    path('change_password', ChangePasswordView.as_view(),),
    path('followers', UserFollowers.as_view(),),
    path('following', UserFollowing.as_view(),)
]