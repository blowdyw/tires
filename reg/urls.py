# reg/urls.py

from django.urls import path
from .views import UserRegisterView, UserLoginView, CustomTokenObtainPairView, UserProfileDetailView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),  # Регистрация пользователя
    path('login/', UserLoginView.as_view(), name='user-login'),  # Вход пользователя
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),  # Получение токенов
    path('profile/', UserProfileDetailView.as_view(), name='user-profile'),  # Получение и обновление профиля пользователя
]
