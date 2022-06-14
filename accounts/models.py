from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)

class Memo(models.Model):
    memo = models.TextField(default='', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  str(self.user) 

class Folder(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Bookmark(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Todo(models.Model):
    text = models.CharField(max_length=20)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField()
    
    def __str__(self):
        return self.text