from django.urls import path, include

from blog.models import Post
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostCategoryView,
    PostLikeView,
)

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='post-edit'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('category/<str:cats>/', PostCategoryView, name='post-category'),
    path('userlike/', PostLikeView, name='post-user-like'),
]

# handler404 = 'blog.views.errorpage'
# handler500 = 'blog.views.errorpage'
