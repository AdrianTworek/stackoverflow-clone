from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from .models import Question, Tag


class QuestionListView(generic.ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        context['questions_count'] = self.get_queryset().count()
        context['page_obj'] = page_obj
        return context


class QuestionDetailView(generic.DetailView):
    model = Question


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ['title', 'content', 'tags']
    template_name = 'questions/question_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Question
    fields = ['title', 'content', 'tags']
    template_name = 'questions/question_update.html'

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    success_url = '/questions'

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author


class TagListView(generic.ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'tags/tag_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(questions_count=Count('questions'))
        queryset = queryset.order_by('-questions_count')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_count'] = self.get_queryset().count()
        return context


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tags/tag_create.html'
    success_url = '/questions/tags'

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower()
        return super().form_valid(form)


class TaggedQuestionListView(generic.ListView):
    model = Question
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.filter(tags__name=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions_count'] = self.get_queryset().count()
        context['tag'] = self.kwargs['slug']
        return context
