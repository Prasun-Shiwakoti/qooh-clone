from django.db import models

# Create your models here.

class users(models.Model):
    username = models.CharField(max_length=100)
    notifications = models.TextField()
    inbox = models.TextField()
    replies = models.TextField()