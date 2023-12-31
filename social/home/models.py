from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.TextField()
    slug=models.SlugField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.slug
    
    def get_absolute_url(self):
        return reverse('home:detail', args=(self.id,self.slug))