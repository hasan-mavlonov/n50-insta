from rest_framework import serializers

from posts.models import PostModel


class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    title = serializers.CharField()
    description = serializers.CharField()

    def validate(self, attrs):
        return attrs

    class Meta:
        model = PostModel
        fields = '__all__'
