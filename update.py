import os
import django
import random
from datetime import date, timedelta

# -------------------------------
# Setup Django environment
# -------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Expense

# -------------------------------
# 1. Clear existing data
# -------------------------------
Expense.objects.all().delete()
User.objects.filter(is_superuser=False).delete()  # Keep superuser if you want
print("Cleared existing Expense and User data (except superuser).")

# -------------------------------
# 2. Create 3 test users
# -------------------------------
user_data = [
    {'username': 'alice', 'email': 'alice@example.com', 'password': 'password123'},
    {'username': 'bob', 'email': 'bob@example.com', 'password': 'password123'},
    {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'password123'},
]

users = []

for u in user_data:
    user = User.objects.create_user(username=u['username'], email=u['email'], password=u['password'])
    users.append(user)
    print(f"User '{u['username']}' created.")

# -------------------------------
# 3. Add realistic expenses
# -------------------------------
categories = ['Food', 'Transport', 'Shopping', 'Entertainment', 'Bills', 'Other']
descriptions = {
    'Food': ['Breakfast', 'Lunch', 'Dinner', 'Coffee', 'Snack'],
    'Transport': ['Bus fare', 'Train ticket', 'Fuel', 'Taxi'],
    'Shopping': ['Clothes', 'Shoes', 'Gadgets', 'Gift'],
    'Entertainment': ['Movie', 'Concert', 'Game', 'Subscription'],
    'Bills': ['Electricity', 'Water', 'Internet', 'Phone'],
    'Other': ['Donation', 'Misc', 'Petrol', 'Health'],
}

for user in users:
    for _ in range(20):
        category = random.choice(categories)
        description = random.choice(descriptions[category])
        amount = round(random.uniform(10, 500), 2)  # Random amount between 10 and 500
        # Random date within last 30 days
        delta_days = random.randint(0, 30)
        expense_date = date.today() - timedelta(days=delta_days)

        Expense.objects.create(
            user=user,
            amount=amount,
            category=category,
            description=description,
            date=expense_date
        )
    print(f"Added 20 expenses for user '{user.username}'.")

print("All data seeded successfully!")
