from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=254)
    subject = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject + ' - ' + self.name
    