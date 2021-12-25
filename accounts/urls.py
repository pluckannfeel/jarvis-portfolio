from django.urls import path, include
from .views import (
    SignUpView,
    AccountDashboardView,
)

app_name = 'account'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('', AccountDashboardView.as_view(), name='account-dashboard'),
]