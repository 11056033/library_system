from django.db import models

class Mood(models.Model):
    status = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.status

class Post(models.Model):
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='不願意透漏身份的人')
    message = models.TextField(null=False)
    del_pass = models.CharField(max_length=10)
    pub_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return self.message

from django.contrib import auth
class Profile(models.Model):
    user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(default=160)
    male = models.BooleanField(default=False)
    website = models.URLField(null=True)
	
    def __str__(self):
        return self.user.username

from django.db import models

class getBook(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title

