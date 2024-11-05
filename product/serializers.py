from rest_framework import serializers
from .models import Category, Product, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductlistSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'main_name',
            'model',
            'photo',
            'price',
            'quantity'
        ]




class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'main_name', 'generated', 'model', 'season',
            'width', 'profile', 'diameter', 'speed_index', 'load_index',
            'double_load_index', 'photo', 'price', 'descriptions',
            'number', 'quantity'
        ]

    def create(self, validated_data):
        # Создаем объект Product с переданными данными
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        # Обновляем поля объекта Product
        if 'category' in validated_data:
            instance.category = validated_data.pop('category')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class FavoriteSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.main_name", read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_name', 'added_at']
        read_only_fields = ['user', 'added_at']
