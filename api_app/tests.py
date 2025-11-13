from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RunTest1APITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.url = reverse('run_test1')

    def test_run_test1_authenticated(self):
        response = self.client.post(
            reverse('token'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('stdout', response.data)
        self.assertIn('stderr', response.data)

    def test_run_test1_unauthenticated(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
