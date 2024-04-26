from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/update/', views.QuestionUpdateView.as_view(),
         name='question_update'),
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(),
         name='question_delete'),
    path('<int:pk>/answers/create/',
         views.AnswerCreateView.as_view(), name='answer_create'),
    path('<int:question_id>/answers/<int:pk>/update/',
         views.AnswerUpdateView.as_view(), name='answer_update'),
    path('<int:question_id>/answers/<int:pk>/delete/',
         views.AnswerDeleteView.as_view(), name='answer_delete'),
    path('tagged/<slug:slug>/', views.TaggedQuestionListView.as_view(),
         name='tagged_question_list'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag_create'),
]
