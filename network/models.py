from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


#Class to keep track of Posts
class Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name="creator")
    title = models.CharField(max_length = 500)
    post = models.TextField()
    liked = models.ManyToManyField(User,blank = True, default = None,related_name="likers")
    time = models.DateTimeField(default = datetime.now())


    def __str__(self):
        return f"{self.user},{self.title},{self.post},{self.liked},{self.time}"


#Class To keep track of Profile
class Profile(models.Model):
    following = models.ForeignKey(User, on_delete = models.CASCADE,related_name="following", blank = True)
    follower = models.ForeignKey(User, on_delete = models.CASCADE,related_name="follower", blank = True)

    def __str__(self):
        return f"{self.follower},{self.following}"


#Class tp keep track of liked posts by users
class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    posts = models.ForeignKey(Post, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user},{self.posts}"
