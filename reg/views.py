# reg/views.py
from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer, UserRegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import UserProfile

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ всем

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерация токенов
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "email": user.email,
            "access": access,
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Генерация токенов
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response({
                "email": user.email,
                "access": access,
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Неверный email или пароль."}, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "email": user.email,  # Добавляем email в ответ
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Неверный email или пароль."}, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

