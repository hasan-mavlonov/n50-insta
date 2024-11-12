from rest_framework import serializers

from posts.models import PostModel, LikeModel, CommentModel


class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    title = serializers.CharField()
    description = serializers.CharField()

    def validate(self, attrs):
        return attrs

    class Meta:
        model = PostModel
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='to_post.title', read_only=True)

    class Meta:
        model = LikeModel
        fields = ['post_title', 'to_post']  # Include 'to_post' for validation purposes

    def validate(self, attrs):
        user = self.context['request'].user
        to_post = attrs.get('to_post')

        # Example validation logic: Check if the user has already liked this post
        if LikeModel.objects.filter(user=user, to_post=to_post).exists():
            raise serializers.ValidationError("You have already liked this post.")

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='to_post.title', read_only=True)

    class Meta:
        model = CommentModel
        fields = ['post_title', 'to_post']  # Include 'to_post' for validation purposes

    def validate(self, attrs):
        user = self.context['request'].user
        to_post = attrs.get('to_post')

        # Example validation logic: Check if the user has already liked this post
        if CommentModel.objects.filter(user=user, to_post=to_post).exists():
            raise serializers.ValidationError("You have already commented this post.")

        return attrs
