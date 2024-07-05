from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    liked_posts = models.ManyToManyField('Post', related_name='likes')

    def __str__(self):
        return f'{self.username}'

class Post(models.Model):
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # One-to-many rel: Post.author & User.posts
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'{self.author}: {self.content}'