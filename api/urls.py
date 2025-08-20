from django.urls import path
from .views import (
    RegisterView, login_view,
    ExpenseListCreateView, ExpenseRetrieveUpdateDeleteView,
    monthly_summary, UserListView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expenses'),
    path('expenses/<int:pk>/', ExpenseRetrieveUpdateDeleteView.as_view(), name='expense-detail'),
    path('summary/monthly/', monthly_summary, name='monthly-summary'),
    path('users/', UserListView.as_view(), name='users-list'),
]
