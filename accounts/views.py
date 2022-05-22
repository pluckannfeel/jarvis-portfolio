from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/account_signup.html'
    
class AccountDashboardView(TemplateView):
    template_name = 'account_dashboard.html'