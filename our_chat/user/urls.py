from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    path('login/', UserRegistrationView.as_view(), name='user-login'),
    
]
