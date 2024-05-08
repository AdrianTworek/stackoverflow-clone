from django.test import TestCase
from ..models import Tag


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
