from django.db import models
from accounts.models import UserModel


class PostModel(models.Model):
    image = models.ImageField(upload_to='posts/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Posts'
        verbose_name = 'Post'


class LikeModel(models.Model):
    to_post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='liked')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='liking')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f"{self.from_user} like {self.to_post}"


class CommentModel(models.Model):
    to_post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='commented')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='commenting')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'

    def __str__(self):
        return f"{self.from_user} comment {self.to_post}"
