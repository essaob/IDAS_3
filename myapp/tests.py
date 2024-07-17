# myapp/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory,Client, override_settings

from IDAS_3.myapp.models import UserProfile


class UserAuthTests(TestCase):

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_form(self):
        user = User.objects.create_user(username='testuser', password='testpassword123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login


class UserProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    def test_create_user_profile(self):
        # Check if a profile already exists for the user
        if not UserProfile.objects.filter(user=self.user).exists():
            UserProfile.objects.create(user=self.user)
        else:
            print("Profile already exists for the user.")

        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
    def test_user_profile_string_representation(self):
        if not UserProfile.objects.filter(user=self.user).exists():
            UserProfile.objects.create(user=self.user)
        else:
            print("Profile already exists for the user.")

        user_profile = UserProfile.objects.get(user=self.user)
        expected_string_representation = f'{self.user.username} Profile'




class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.factory = RequestFactory()
