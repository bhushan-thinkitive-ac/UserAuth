from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, UserSendPasswordResetEmailView,UserPasswordResetView
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('send_reset_password_email/', UserSendPasswordResetEmailView.as_view(), name='send_reset_password_email'),
    path('reset_password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]