from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Tag, Question, Answer, QuestionVote, AnswerVote


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='Django')

    def test_name_label(self):
        tag = Tag.objects.get(id=1)
        field_label = tag._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        tag = Tag.objects.get(id=1)
        max_length = tag._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_name(self):
        tag = Tag.objects.get(id=1)
        expected_object_name = tag.name
        self.assertEqual(expected_object_name, str(tag))


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        Question.objects.create(
            title='Test question', content='Test content', author=User.objects.get(id=1))

    def test_title_label(self):
        question = Question.objects.get(id=1)
        title_label = question._meta.get_field('title').verbose_name
        self.assertEqual(title_label, 'title')

    def test_title_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_content_label(self):
        question = Question.objects.get(id=1)
        content_label = question._meta.get_field('content').verbose_name
        self.assertEqual(content_label, 'content')

    def test_object_name_is_title(self):
        question = Question.objects.get(id=1)
        expected_object_name = question.title
        self.assertEqual(expected_object_name, str(question))

    def test_get_absolute_url(self):
        question = Question.objects.get(id=1)
        self.assertEqual(question.get_absolute_url(), '/questions/1/')


class AnswerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        Question.objects.create(
            title='Test question', content='Test content', author=User.objects.get(id=1))
        Answer.objects.create(
            content='Test answer', question=Question.objects.get(id=1), author=User.objects.get(id=1))

    def test_content_label(self):
        answer = Answer.objects.get(id=1)
        content_label = answer._meta.get_field('content').verbose_name
        self.assertEqual(content_label, 'content')

    def test_object_name_is_question_title(self):
        answer = Answer.objects.get(id=1)
        expected_object_name = f"Answer to '{answer.question.title}'"
        self.assertEqual(expected_object_name, str(answer))


class QuestionVoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        Question.objects.create(
            title='Test question', content='Test content', author=User.objects.get(id=1))

    def test_toggle_vote(self):
        question = Question.objects.get(id=1)
        user = User.objects.get(id=1)
        vote = QuestionVote.objects.create(
            question=question, user=user, is_upvote=True)
        self.assertEqual(vote.is_upvote, True)
        vote.is_upvote = False
        vote.save()
        self.assertEqual(vote.is_upvote, False)

    def test_question_user_unique_together(self):
        question = Question.objects.get(id=1)
        user = User.objects.get(id=1)
        QuestionVote.objects.create(
            question=question, user=user, is_upvote=True)
        with self.assertRaises(Exception):
            QuestionVote.objects.create(
                question=question, user=user, is_upvote=False)


class AnswerVoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        Question.objects.create(
            title='Test question', content='Test content', author=User.objects.get(id=1))
        Answer.objects.create(
            content='Test answer', question=Question.objects.get(id=1), author=User.objects.get(id=1))

    def test_toggle_vote(self):
        answer = Answer.objects.get(id=1)
        user = User.objects.get(id=1)
        vote = AnswerVote.objects.create(
            answer=answer, user=user, is_upvote=True)
        self.assertEqual(vote.is_upvote, True)
        vote.is_upvote = False
        vote.save()
        self.assertEqual(vote.is_upvote, False)

    def test_answer_user_unique_together(self):
        answer = Answer.objects.get(id=1)
        user = User.objects.get(id=1)
        AnswerVote.objects.create(
            answer=answer, user=user, is_upvote=True)
        with self.assertRaises(Exception):
            AnswerVote.objects.create(
                answer=answer, user=user, is_upvote=False)
