import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import RegisterForm, UserUpdateForm, ProfileUpdateForm


class RegisterFormTest(TestCase):
    def test_empty_form(self):
        form = RegisterForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)

    def test_register_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalid_email',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_passwords_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'invalid_password',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_passwords_too_short(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProfileUpdateFormsTest(TestCase):

    def test_user_update_empty_form(self):
        form = UserUpdateForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)

    def test_profile_update_empty_form(self):
        form = ProfileUpdateForm()
        self.assertIn('bio', form.fields)
        self.assertIn('image', form.fields)

    def test_user_update_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
        }
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_update_form(self):
        image_path = os.path.abspath(os.path.join(os.path.dirname(
            __file__), '..', '..', 'media', 'default_user_image.jpg'))
        with open(image_path, 'rb') as f:
            image_content = f.read()
            image = SimpleUploadedFile(
                name='test_image.jpg', content=image_content, content_type='image/jpeg')

        form_data = {
            'bio': 'test bio',
            'image': image,
        }
        form = ProfileUpdateForm(data=form_data, files=form_data)
        self.assertTrue(form.is_valid())
