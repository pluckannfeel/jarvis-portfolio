from django.contrib import admin
from .models import Post, Category, Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0 # change how many comments you want to see on post 

class PostListAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]
    list_display = ['id', 'title', 'category', 'author']

admin.site.register(Post, PostListAdmin)
admin.site.register(Category)
admin.site.register(Comment)