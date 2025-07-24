from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200 , null=True)
    email = models.EmailField(max_length=200 , unique=True , null=True)
    bio = models.TextField(default='no bio...' , null=True)

    avatar = models.ImageField(null=True , blank=True , default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)
    

    def __str__(self):
        return self.name

# class Topic(models.Model):
#     # A topic can have multiple rooms    But a room can have only one topic          One to Many
#     name = models.CharField(max_length=200)
#     #updated = models.DateTimeField(auto_now=True)
#     #created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.name

class Room(models.Model):
    host = models.ForeignKey(User , on_delete=models.CASCADE , null=True)
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL , null=True) # One to Many connected to Topic
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    participants = models.ManyToManyField(User , related_name='participants' , blank=True) # Many to Many connected to User
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']     # Order by updated and created i.e. latest first

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    room =models.ForeignKey(Room , on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']     # Order by updated and created i.e. latest first


    def __str__(self):
        return self.body[:50]
