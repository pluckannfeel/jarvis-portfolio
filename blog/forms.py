from django import forms
from .models import Post, Category, Comment
from django.contrib.auth import get_user_model

category_choices = Category.objects.all().values_list('name', 'name')
choices = []
for item in category_choices:
    choices.append(item)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 
            'body',
            'category',
            'header_image'
        ]
        
        labels = {
            "title": "Post Title",
            "body": "Write a Content.."
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'contact_input'}),
            'body': forms.Textarea(attrs={'class': 'contact_input', 'rows': '10'}),
            'category': forms.Select(choices=choices, attrs={'class': 'contact_input'}),
            'header_image': forms.FileInput(attrs={'class': 'contact_input'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(PostCreateForm, self).__init__(*args, **kwargs)
    
        
    def save(self, *args, **kwargs):
        kwargs['commit']=False
        obj = super(PostCreateForm, self).save(*args, **kwargs)
        if self.request:
            obj.author = self.request.user
            obj.save()
        return obj 
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title
        
    def clean_body(self):
        body = self.cleaned_data.get('body')
        return body
    
    # def clean_tag(self):
    #     tag = self.cleaned_data.get('tag')
    #     return tag
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category
    
    def clean_header_image(self):
        header_image = self.cleaned_data.get('header_image')
        return header_image
    
class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 
            'body',
            'category',
            # 'header_image' temporarily remove header image field on update post form
        ]
        
        labels = {
            "title": "Post Title",
            "body": "Write a Content.."
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'contact_input'}),
            'body': forms.Textarea(attrs={'class': 'contact_input', 'rows': '10'}),
            'category': forms.Select(choices=choices, attrs={'class': 'contact_input'}),
            # 'header_image': forms.FileInput(attrs={'class': 'contact_input'}),
        }

class PostAddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment', 
        ]
        
        labels = {
            "comment": "Write a Comment.."
        }
        
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'contact_input', 'rows': '2'}),
        }