from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileView, ProfileUpdateView

app_name = "user"

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-profile/',ProfileUpdateView.as_view() , name='update-profile')
    
]
