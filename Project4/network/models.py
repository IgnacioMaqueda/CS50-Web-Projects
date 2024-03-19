from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.id}: From {self.poster} at {self.timestamp} with {self.likes} likes"

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }


class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followings")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}: {self.follower} followed {self.following} at {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "follower": self.follower,
            "following": self.following,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    def is_valid_follow(self):
        return self.follower != self.following
    

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="liked")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}: {self.user} liked {self.post} at {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "post": self.post,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
