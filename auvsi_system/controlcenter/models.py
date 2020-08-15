from django.db import models

# Create your models here.

class InteropServer(models.Model):
    url = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    def __str__(self):
        return "InteropServer"