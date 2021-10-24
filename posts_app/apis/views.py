from django.db.models import Q, query
from posts_app.models import Posts
from rest_framework import generics, status
from .serializers import PostsSerializer
from user_app.models import Account as User
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class PostsCustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class PostsView(generics.ListCreateAPIView):
    serializer_class = PostsSerializer
    pagination_class = PostsCustomPagination

    def get_queryset(self):
        query_set = Posts.my_posts(self.request.user)
        return query_set
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PostsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFeedsView(generics.ListAPIView):
    serializer_class = PostsSerializer
    pagination_class = PostsCustomPagination

    def get_queryset(self):
        query_set = Posts.get_feeds(self.request.user)
        return query_set


