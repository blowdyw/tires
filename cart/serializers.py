from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.main_name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    image_url = serializers.URLField(read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)  # ID продукта, для удобства

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'total_price', 'image_url', 'product_id']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Добавляем итоговую сумму

    class Meta:
        model = Cart
        fields = ['id', 'created', 'total_price', 'items']  # Включаем total_price и items для корзины
