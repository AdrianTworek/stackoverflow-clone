from django.contrib import admin
from users.models import Profile
from questions.models import Question

admin.site.register([Profile, Question])
