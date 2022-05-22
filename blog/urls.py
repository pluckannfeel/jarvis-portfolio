from django.urls import path, include

from blog.models import Post
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostCategoryView,
    PostAddLike,
    PostAddComment,
)

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='post-edit'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('category/<str:cats>/', PostCategoryView, name='post-category'),

    # ajax urls
    path('userlike/', PostAddLike, name='post-user-like'),
    path('usercomment/', PostAddComment, name='post-user-comment'),
]

# handler404 = 'blog.views.errorpage'
# handler500 = 'blog.views.errorpage'
