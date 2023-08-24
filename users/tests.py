from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationView(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
            'username': 'Test_username', 'email': 'test_email@gmail.com',
            'password1': '12345678pP', 'password2': '12345678pP',
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Registration')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())  # user not exists in system before request
        response = self.client.post(self.path, self.data)

        # check user creating
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302 code
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())  # user exists in system after request

        # check email verification creating
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)
