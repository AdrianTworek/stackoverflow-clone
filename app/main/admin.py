from django.contrib import admin
from users.models import Profile
from questions.models import Question, Tag, Answer, QuestionVote, AnswerVote, QuestionView

admin.site.register([Profile, Question, Tag, Answer,
                    QuestionVote, AnswerVote, QuestionView])
