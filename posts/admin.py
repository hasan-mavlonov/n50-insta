from django.contrib import admin

from posts.models import PostModel, LikeModel, CommentLikeModel, CommentModel


@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'description',)


@admin.register(LikeModel)
class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'to_post')


@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'to_post')


admin.site.register(CommentLikeModel)
