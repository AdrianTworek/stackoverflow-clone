from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
]
