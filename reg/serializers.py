# reg/serializers.py

from rest_framework import serializers
from .models import CustomUser, UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email']
        )
        user.set_password(validated_data['password1'])
        user.save()

        # Создаем профиль пользователя
        UserProfile.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Пользователь с таким email не найден.")

            if not user.check_password(password):
                raise serializers.ValidationError("Неверный пароль.")

            attrs['user'] = user
        else:
            raise serializers.ValidationError("Email и пароль обязательны.")

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'name', 'surname', 'patronymic', 'number']
        read_only_fields = ['user']  # Запретить изменение пользователя через API

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance
