from django.db import models

class Posts(models.Model):
    content = models.TextField()  
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

