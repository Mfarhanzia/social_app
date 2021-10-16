from django.urls import path
from django.urls.conf import include
# from rest_framework import routers
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from user_app.apis.views import UserApis, UserFollowers


router = routers.DefaultRouter()
router.register(r'', UserApis, basename='user')  #User apis
router.register(r'follower', UserFollowers, basename='followers')  #User apis

urlpatterns = [
    path('', include(router.urls)),
]