from django.contrib import admin
from .models import Post, Category

# Register your models here.

class PostListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'author']

admin.site.register(Post, PostListAdmin)
admin.site.register(Category)