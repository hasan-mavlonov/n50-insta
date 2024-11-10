from django.urls import path
from posts import views
app_name = 'posts'
urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
]