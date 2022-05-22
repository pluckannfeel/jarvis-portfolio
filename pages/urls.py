from django.urls import path
from .views import HomePageView, SubmitContact
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pages'
urlpatterns = [
    path('contact_submit/', SubmitContact, name='contact-submit'),
    path('', HomePageView.as_view(), name='home'),
]