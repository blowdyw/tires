from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Возвращает корзину текущего пользователя."""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Добавляет товар в корзину текущего пользователя."""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        # Проверка на положительное количество
        if quantity <= 0:
            return Response({"error": "Quantity must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка наличия товара
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Проверка наличия достаточного количества товара на складе
        if product.quantity < quantity:
            return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)

        # Добавляем товар в корзину или увеличиваем количество
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, user=request.user)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        # Возвращаем обновленную корзину
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def apply_discount(self, request):
        """Применяет скидку к корзине текущего пользователя."""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        discount = float(request.data.get('discount', 0))

        # Проверка на допустимость скидки
        if discount < 0 or discount > cart.total_price:
            return Response({"error": "Invalid discount amount."}, status=status.HTTP_400_BAD_REQUEST)

        # Применение скидки
        cart.discount = discount
        cart.save()

        # Возвращаем обновленную корзину
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
