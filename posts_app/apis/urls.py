from django.urls import path
from django.urls.conf import include
# from rest_framework import routers
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import PostsView, GetFeedsView


urlpatterns = [
    path('', PostsView.as_view(),),
    path('feed', GetFeedsView.as_view(),)
]