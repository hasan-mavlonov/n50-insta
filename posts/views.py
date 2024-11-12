from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import PostModel, LikeModel, CommentModel
from posts.serializers import PostCreateSerializer, PostListSerializer, LikeSerializer, CommentSerializer


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = PostCreateSerializer
    queryset = PostModel.objects.all()

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        post.save()
        return post


class PostListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = PostListSerializer

    def get_queryset(self):
        return PostModel.objects.filter(user=self.request.user)


class PostEditView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer

    def perform_update(self, serializer):
        post = serializer.save(user=self.request.user)
        post.save()
        return post


class PostDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    post = None

    def get_queryset(self):
        return PostModel.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.post = self.get_object()
        self.post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = LikeModel.objects.all()
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
