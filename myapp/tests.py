# tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ContactUsForm
from .models import Contact


class UserAuthenticationTests(TestCase):

    def setUp(self):
        self.signup_url = reverse('signupuser')
        self.login_url = reverse('loginuser')
        self.contactus_url = reverse('contactus')
        self.profile_url = reverse('profile')

        self.user = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }

        self.user_instance = User.objects.create_user(**self.user)

    def test_signup_page(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_post(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post(self):
        response = self.client.post(self.login_url, {
            'username': self.user['username'],
            'password': self.user['password']
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_contactus_page(self):
        response = self.client.get(self.contactus_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactus.html')

    def test_contactus_post(self):
        form_data = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(self.contactus_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Message was sent successfully')

    def test_profile_page(self):
        self.client.login(username=self.user['username'], password=self.user['password'])
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login if not authenticated
