from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Expense
from .serializers import UserSerializer, ExpenseSerializer

User = get_user_model()

# ----------------------
# Registration
# ----------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ----------------------
# Login
# ----------------------
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email') or request.POST.get('email')
    password = request.data.get('password') or request.POST.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=400)

    try:
        user_obj = User.objects.get(email=email)
        user = authenticate(username=user_obj.username, password=password)
    except User.DoesNotExist:
        user = None

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email
        })
    return Response({'error': 'Invalid Credentials'}, status=400)

# ----------------------
# Pagination class
# ----------------------
class ExpensePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

# ----------------------
# Expense List & Create
# ----------------------
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ExpensePagination

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        start = self.request.query_params.get('startDate')
        end = self.request.query_params.get('endDate')
        category = self.request.query_params.get('category')
        if start and end:
            queryset = queryset.filter(date__range=[start, end])
        if category:
            queryset = queryset.filter(category=category)
        sort_by = self.request.query_params.get('sort', 'date')
        if sort_by not in ['date', 'amount']:
            sort_by = 'date'
        return queryset.order_by(sort_by)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ----------------------
# Expense Retrieve / Update / Delete
# ----------------------
class ExpenseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

# ----------------------
# Monthly Summary
# ----------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def monthly_summary(request):
    expenses = Expense.objects.filter(user=request.user)
    summary = expenses.annotate(month=TruncMonth('date')) \
        .values('month', 'category') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('month')
    return Response(summary)

# ----------------------
# Users List (optional for admin)
# ----------------------
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
