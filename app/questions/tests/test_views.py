from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Question, QuestionVote, Answer, AnswerVote


class QuestionViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(username='testuser', password='testpassword')

    def test_question_list_view(self):
        response = self.client.get(reverse('main:questions:question_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_list.html')

    def test_question_create_view(self):
        response = self.client.get(reverse('main:questions:question_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_create.html')

        form_data = {
            'title': 'Test question',
            'content': 'Test content',
        }
        response = self.client.post(
            reverse('main:questions:question_create'), data=form_data)
        self.assertRedirects(response, reverse(
            'main:questions:question_detail', args=[1]))

    def test_question_detail_view(self):
        Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        response = self.client.get(
            reverse('main:questions:question_detail', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_detail.html')

    def test_question_update_view(self):
        Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        response = self.client.get(
            reverse('main:questions:question_update', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_update.html')

        form_data = {
            'title': 'Updated question',
            'content': 'Updated content',
        }
        response = self.client.post(
            reverse('main:questions:question_update', args=[1]), data=form_data)
        self.assertRedirects(response, reverse(
            'main:questions:question_detail', args=[1]))

    def test_question_delete_view(self):
        Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        response = self.client.get(
            reverse('main:questions:question_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.client.post(
            reverse('main:questions:question_delete', args=[1]))
        response = self.client.get(
            reverse('main:questions:question_detail', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_question_vote_view(self):
        question = Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        response = self.client.post(
            reverse('main:questions:question_vote', args=[1]), {'vote': 'up'})
        self.assertRedirects(response, reverse(
            'main:questions:question_detail', args=[1]))
        self.assertEqual(QuestionVote.objects.filter(
            question=question, is_upvote=True).count(), 1)

        response = self.client.post(
            reverse('main:questions:question_vote', args=[1]), {'vote': 'down'})
        self.assertRedirects(response, reverse(
            'main:questions:question_detail', args=[1]))
        self.assertEqual(QuestionVote.objects.filter(
            question=question, is_upvote=True).count(), 0)


class TagViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(username='testuser', password='testpassword')

    def test_tag_create_view(self):
        response = self.client.get(reverse('main:questions:tag_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tags/tag_create.html')

        form_data = {
            'name': 'django',
        }
        response = self.client.post(
            reverse('main:questions:tag_create'), data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_tag_list_view(self):
        response = self.client.get(reverse('main:questions:tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tags/tag_list.html')

    def test_tagged_question_list_view(self):
        response = self.client.get(
            reverse('main:questions:tagged_question_list', args=['django']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_list.html')


class AnswerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(username='testuser', password='testpassword')

    def test_answer_create_view(self):
        Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        response = self.client.get(
            reverse('main:questions:answer_create', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'answers/answer_create.html')

        form_data = {
            'content': 'Test answer',
        }
        response = self.client.post(
            reverse('main:questions:answer_create', args=[1]), data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_answer_update_view(self):
        Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        Answer.objects.create(
            content='Test answer', question=Question.objects.get(id=1), author=self.user
        )
        response = self.client.get(
            reverse('main:questions:answer_update', args=[1, 1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'answers/answer_update.html')

        form_data = {
            'content': 'Updated answer',
        }
        self.client.post(
            reverse('main:questions:answer_update', args=[1, 1]), data=form_data)
        answer = Question.objects.get(id=1).answers.first()
        self.assertEqual(answer.content, 'Updated answer')

    def test_answer_delete_view(self):
        Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        Answer.objects.create(
            content='Test answer', question=Question.objects.get(id=1), author=self.user
        )
        self.client.post(
            reverse('main:questions:answer_delete', args=[1, 1]))
        response = self.client.get(
            reverse('main:questions:question_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.get(id=1).answers.count(), 0)

    def test_answer_vote_view(self):
        question = Question.objects.create(
            title='Test question', content='Test content', author=self.user
        )
        answer = Answer.objects.create(
            content='Test answer', question=question, author=self.user
        )
        response = self.client.post(
            reverse('main:questions:answer_vote', args=[1, 1]), {'vote': 'up'})
        self.assertRedirects(response, reverse(
            'main:questions:question_detail', args=[1]))
        self.assertEqual(AnswerVote.objects.filter(
            answer=answer, is_upvote=True).count(), 1)

        response = self.client.post(
            reverse('main:questions:answer_vote', args=[1, 1]), {'vote': 'down'})
        self.assertRedirects(response, reverse(
            'main:questions:question_detail', args=[1]))
        self.assertEqual(AnswerVote.objects.filter(
            answer=answer, is_upvote=True).count(), 0)
