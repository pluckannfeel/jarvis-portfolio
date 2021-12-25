# rendering, get object list and redirect classes, reverse for url utility funcs
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.db.models import Count

import json

# view functions
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# models
from .models import Post, Category
from django.db.models import F

#form
from .forms import PostCreateForm, PostUpdateForm

# instead importing user, import the custom user from abstract user class we created
from django.contrib.auth import get_user_model

#mixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    ordering = ['-date']
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = get_category_list()
        context['recent_posts'] = get_recent_posts()
        return context
        
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        
        post_object = get_object_or_404(Post, id=self.kwargs['pk'])
        context['categories'] = get_category_list()
        context['total_likes'] = post_object.total_likes()
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create.html'
    # __all__ fills up all inputs on models
    
    def get_form_kwargs(self):
        # Ensure the current `request` is provided to NonProfitCreateForm.
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs.update({ 'request': self.request })
        return kwargs

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    form_class = PostUpdateForm
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('blog:post-list')
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
def PostCategoryView(request, cats):
    category_posts = Post.objects.select_related('category').annotate(category_name=F('category__name')).filter(category_name__iexact=cats).order_by('-date')
    count_posts = category_posts.count()
    
    if count_posts == 0:
        return Http404
    
    context = {
        'category_name': cats,
        'category_posts': category_posts,
        'post_count': count_posts,
        'recent_posts': get_recent_posts(),
        'categories': get_category_list(),
    }
    
    return render(request, 'post_categories.html', context)

def PostLikeView(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            like_data = data.get('payload')
            post_id = like_data['post_id']
            postobj = get_object_or_404(Post, id=post_id)
            postobj.likes.add(request.user)
            return JsonResponse({'status': 'Contact Submitted!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
    
    # return HttpResponseRedirect(reverse('blog:post-detail', kwargs={"pk": pk}))


def get_category_list():
    # category bar with number of posts
    categories_list = Category.objects.annotate(posts_count=Count('post'))
    return categories_list

def get_recent_posts():
    # recent post with limit of 3 recent post
    recentposts_list = Post.objects.all().order_by('-date')[:3]
    return recentposts_list
    
        