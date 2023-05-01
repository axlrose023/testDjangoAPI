from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from restaurant.models import Restaurant, Menu
from restaurant.serializers import RestaurantSerializer, MenuSerializer

User = get_user_model()


# Create your tests here.
class RestApiTest(TestCase):
    def test_create_restaurant(self):
        user = User.objects.create_user(name='testuser', email='testuser@test.com', password='Test123')
        restaurant = Restaurant.objects.create(name='Test Restaurant', owner=user)
        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.name, 'Test Restaurant')
        self.assertEqual(restaurant.owner, user)

    def test_create_menu(self):
        user = User.objects.create_user(name='testuser', email='testuser@test.com', password='Test123')
        restaurant = Restaurant.objects.create(name='Test Restaurant', owner=user)
        menu = Menu.objects.create(restaurant=restaurant, items='Test Item 1\nTest Item 2\nTest Item 3')
        self.assertIsNotNone(menu)
        self.assertEqual(menu.restaurant, restaurant)
        self.assertEqual(menu.date, date.today())
        self.assertEqual(menu.items, 'Test Item 1\nTest Item 2\nTest Item 3')

    def test_serialize_restaurant(self):
        user = User.objects.create_user(name='testuser', email='testuser@test.com', password='Test123')
        restaurant = Restaurant.objects.create(name='Test Restaurant', owner=user)
        serializer = RestaurantSerializer(restaurant)
        expected_data = {
            'name': 'Test Restaurant',
            'owner': user.id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serialize_menu(self):
        user = User.objects.create_user(name='testuser', email='testuser@test.com', password='Test123')
        restaurant = Restaurant.objects.create(name='Test Restaurant', owner=user)
        menu = Menu.objects.create(restaurant=restaurant, items='Test Item 1\nTest Item 2\nTest Item 3')
        serializer = MenuSerializer(menu)
        expected_data = {
            'items': 'Test Item 1\nTest Item 2\nTest Item 3',
            'restaurant': restaurant.id,
        }
        self.assertEqual(serializer.data, expected_data)

