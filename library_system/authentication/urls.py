
from django.urls import path

from authentication.Views import SignIn


urlpatterns = [
    path('home', SignIn.SignIn.as_view(), name='SignIn'),
]


