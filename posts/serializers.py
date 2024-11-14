from rest_framework import serializers

from posts.models import PostModel, LikeModel, CommentModel, CommentLikeModel


class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    title = serializers.CharField()
    description = serializers.CharField()

    def validate(self, attrs):
        return attrs

    class Meta:
        model = PostModel
        fields = ['image', 'title', 'description']

    def validate(self, attrs):
        user = self.context['request'].user
        image = attrs.get('image')
        title = attrs.get('title')
        description = attrs.get('description')
        return attrs


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
    content = serializers.CharField()

    class Meta:
        model = CommentModel
        fields = ['post_title', 'to_post', 'content']

    def validate(self, attrs):
        user = self.context['request'].user
        to_post = attrs.get('to_post')
        content = attrs.get('content')

        if CommentModel.objects.filter(user=user, to_post=to_post).exists():
            raise serializers.ValidationError("You have already commented this post.")
        if PostModel.objects.filter(title=to_post, user=user).exists():
            raise serializers.ValidationError("You can't comment your own post.")
        return attrs


class CommentLikeSerializer(serializers.ModelSerializer):
    comment_title = serializers.CharField(source='to_comment.title', read_only=True)

    class Meta:
        model = CommentLikeModel
        fields = ['comment_title', 'to_comment']

    def validate(self, attrs):
        user = self.context['request'].user
        to_comment = attrs.get('to_comment')
        if CommentLikeModel.objects.filter(user=user, to_comment=to_comment).exists():
            raise serializers.ValidationError("You have already liked this comment.")
        return attrs
