from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import AbstractModel


class Tag(AbstractModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(AbstractModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:questions:question_detail", kwargs={"pk": self.pk})


class QuestionView(AbstractModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.CharField(max_length=50)


class Answer(AbstractModel):
    content = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer to '{self.question.title}'"


class QuestionVote(AbstractModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ['question', 'user']


class AnswerVote(AbstractModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ['answer', 'user']
