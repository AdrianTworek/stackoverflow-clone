from django.db import models
from django.contrib.auth.models import User
from main.models import AbstractModel


class Question(AbstractModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
