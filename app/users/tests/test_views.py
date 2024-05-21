from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse('main:users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(
            reverse('main:users:register'), data=form_data)
        self.assertRedirects(response, reverse('main:home'))

    def test_register_view_invalid_data(self):
        response = self.client.get(reverse('main:users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

        invalid_form_data = {
            'username': '',
            'email': 'test@',
            'password1': 'testpassword',
            'password2': 'invalid_password',
        }
        response = self.client.post(
            reverse('main:users:register'), data=invalid_form_data)
        self.assertContains(response, 'This field is required.')
        self.assertContains(response, 'Enter a valid email address.')
        self.assertContains(response, 'The two password fields didn’t match.')

    def test_login_view(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        response = self.client.get(reverse('main:users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(
            reverse('main:users:login'), data=form_data)
        self.assertRedirects(response, reverse('main:home'))

    def test_login_view_invalid_data(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        response = self.client.get(reverse('main:users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        invalid_form_data = {
            'username': 'testuser',
            'password': '',
        }
        response = self.client.post(
            reverse('main:users:login'), data=invalid_form_data)
        self.assertContains(response, 'This field is required.')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('main:users:logout'))
        self.assertRedirects(response, reverse('main:users:login'))
