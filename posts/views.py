from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import PostModel
from posts.serializers import PostCreateSerializer


class PostCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = PostCreateSerializer
    queryset = PostModel.objects.all()

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        post.save()
        return post
