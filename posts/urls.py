from django.urls import path
from posts import views

app_name = 'posts'
urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('list/', views.PostListView.as_view(), name='list_post'),
    path('edit/<pk>', views.PostEditView.as_view(), name='edit_post'),
    path('delete/<pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('liked/', views.LikeView.as_view(), name='like_post'),
    path('commented/', views.CommentView.as_view(), name='comment_post'),
    path('comment_like/', views.CommentLikeView.as_view(), name='like_comment')
]
