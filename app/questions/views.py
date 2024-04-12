from django.shortcuts import render
from django.views import generic
from .models import Question


class QuestionListView(generic.ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-created_at']
    template_name = 'question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions_count'] = self.get_queryset().count()
        return context
