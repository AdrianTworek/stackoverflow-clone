from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import AbstractModel


class Question(AbstractModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:questions:question_detail", kwargs={"pk": self.pk})
