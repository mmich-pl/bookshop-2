from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserAccountTests(TestCase):
    def setUp(self):
        self.user_class = get_user_model()
        self.register_url = reverse('core-api:auth-register-list')

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'username', 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.username, 'username')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "username")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testsuperuser@super.com', username='username1', password='password',
                is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testsuperuser@super.com', username='username1', password='password',
                is_staff=False)

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.username, 'username')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)


        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', username='username1', password='password', is_superuser=True)

    def test_register_complete_data(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(self.user_class.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], data['username'])
        self.assertEqual(response.data['user']['email'], data['email'])
        self.assertEqual(response.data['user']['is_active'], True)
        self.assertFalse('password' in response.data)

    def test_register_short_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'pass'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(self.user_class.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': ''
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(self.user_class.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_too_long_username(self):
        data = {
            'username': 'famcybqeioufnevblmks1',
            'email': 'foobar@example.com',
            'password': 'zaq1@WSXchu09-'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(self.user_class.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_username(self):
        data = {
            'username': '',
            'email': 'foobar@example.com',
            'password': 'zaq1@WSXchu09-'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(self.user_class.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_email(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'zaq1@WSXchu09-'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(self.user_class.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_preexisting_username(self):
        user = self.user_class.objects.create_user(
            'testuser@user.com', 'foobar', 'password')
        user.save()

        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'zaq1@WSXchu09-'
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(self.user_class.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
