from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')

    def test_bio_label(self):
        profile = Profile.objects.filter(user=User.objects.get(id=1)).first()
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')

    def test_bio_max_length(self):
        profile = Profile.objects.filter(user=User.objects.get(id=1)).first()
        max_length = profile._meta.get_field('bio').max_length
        self.assertEqual(max_length, 500)

    def test_profile_user_unique(self):
        # should throw an error, because Profile is always created during User creation
        with self.assertRaises(Exception):
            Profile.objects.create(user=User.objects.get(id=1))

    def test_object_name_is_username(self):
        profile = Profile.objects.filter(user=User.objects.get(id=1)).first()
        expected_object_name = profile.user.username
        self.assertEqual(f"{expected_object_name}'s Profile", str(profile))
