from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from .models import Question, Tag, Answer, QuestionVote


class QuestionListView(generic.ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return Question.objects.all().order_by('-created_at')
        return Question.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        context['questions_count'] = self.get_queryset().count()
        context['page_obj'] = page_obj
        return context


class QuestionDetailView(generic.DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        question_votes = QuestionVote.objects.filter(question=question)
        upvotes_count = question_votes.filter(is_upvote=True).count()
        downvotes_count = question_votes.filter(is_upvote=False).count()
        question_votes_number = upvotes_count - downvotes_count
        user_vote = question_votes.filter(user=self.request.user).first()
        context['question_votes_number'] = question_votes_number
        context['user_vote'] = user_vote
        context['answers'] = question.answers.all().order_by('-created_at')
        return context


class QuestionVoteView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        user = request.user
        is_upvote = request.POST.get('vote') == 'up'
        question_vote = QuestionVote.objects.filter(
            question=question, user=user).first()
        if question_vote:
            if question_vote.is_upvote == is_upvote:
                question_vote.delete()
            else:
                question_vote.is_upvote = is_upvote
                question_vote.save()
        else:
            QuestionVote.objects.create(
                question=question, user=user, is_upvote=is_upvote)
        return redirect('main:questions:question_detail', pk=question.pk)


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
        return Question.objects.filter(tags__name=self.kwargs['slug']).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions_count'] = self.get_queryset().count()
        context['tag'] = self.kwargs['slug']
        return context


class AnswerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Answer
    fields = ['content']
    template_name = 'answers/answer_create.html'

    def form_valid(self, form):
        form.instance.question = Question.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f"/questions/{self.kwargs['pk']}"


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Answer
    fields = ['content']
    template_name = 'answers/answer_update.html'

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author

    def get_success_url(self):
        question_id = self.kwargs['question_id']
        return f"/questions/{question_id}"


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Answer

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author

    def get_success_url(self):
        question_id = self.kwargs['question_id']
        return f"/questions/{question_id}"
