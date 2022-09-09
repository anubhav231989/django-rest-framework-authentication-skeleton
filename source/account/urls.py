from django.urls import path
from account.apis import UserRegistration, UserLogin, UserProfile, UserPasswordChange, UsersView


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
    path('password/change/', UserPasswordChange.as_view(), name='user_password_change'),
    path('list/', UsersView.as_view(), name='users'),
]