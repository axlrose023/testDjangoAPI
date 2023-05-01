from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .views import EmployeeView, LoginView, index, vote, votes, MenuView
from datetime import datetime, timezone
from unittest import mock

from django.urls import reverse

from employee.models import Vote
from restaurant.models import Restaurant, Menu

User = get_user_model()


class VoteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            owner=self.user
        )

        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            items='Test menu items'
        )

    def test_vote_creation(self):
        vote = Vote.objects.create(
            employee=self.user,
            menu=self.menu
        )

        self.assertEqual(vote.employee, self.user)
        self.assertEqual(vote.menu, self.menu)
        self.assertIsNotNone(vote.date)


class EmployeeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_employee_creation_view(self):
        url = reverse('employee_creation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

        response = self.client.post(url, {'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertTrue(User.objects.filter(email='test@test.com').exists())

        response = self.client.post(url, {'email': '', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertFalse(User.objects.filter(email='').exists())

    def tearDown(self):
        User.objects.all().delete()


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test@test.com', password='testpass')

    def test_login_view(self):
        url = reverse('employee_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(url, {'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

        response = self.client.post(url, {'email': 'wrongemail@test.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def tearDown(self):
        User.objects.all().delete()
