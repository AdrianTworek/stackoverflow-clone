from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Tag, Question


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
