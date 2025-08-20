from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Expense

class ExpenseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_expense(self):
        data = {'amount': 50, 'category': 'Food', 'description': 'Lunch', 'date': '2025-08-21'}
        response = self.client.post('/api/expenses/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.count(), 1)