from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question


class QuestionListView(generic.ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions_count'] = self.get_queryset().count()
        return context


class QuestionDetailView(generic.DetailView):
    model = Question


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ['title', 'content']
    login_url = 'main:users:login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
