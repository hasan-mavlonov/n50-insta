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
