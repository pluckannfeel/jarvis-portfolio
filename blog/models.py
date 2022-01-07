from django.contrib import auth
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
import os

#  Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver

class Category(models.Model):
    name = models.CharField(max_length=225)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="uploads/")
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    # body = models.TextField()
    body = RichTextField(blank=True, null=True)
    # category = models.CharField(max_length=64, default="Uncategorized")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(), related_name='blog_posts', null=True, blank=True)
    

    def total_comments(self):
        return self.comments.count()

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={"pk":  self.pk})

    def delete(self):
        self.header_image.delete()
        super(Post, self).delete()

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='comments',
        )
    comment = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={"pk":  self.pk})
    

def _delete_file(path):
#    """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=Post)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.header_image:
        _delete_file(instance.header_image.path)