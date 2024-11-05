from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Favorite
from .serializers import CategorySerializer, ProductSerializer, FavoriteSerializer, ProductlistSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductlistSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # Сохраняем продукт, метод save() возвращает созданный объект
        product = serializer.save()

        # Вызываем метод super(), чтобы вернуть стандартный ответ, который будет включать созданный объект
        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_201_CREATED
        )


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращает только избранные продукты текущего пользователя
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # При создании записи, добавляем текущего пользователя в поле user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        # Проверяем, добавлен ли уже продукт в избранное
        if Favorite.objects.filter(user=request.user, product_id=product_id).exists():
            return Response(
                {"detail": "Этот продукт уже добавлен в избранное."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

# class PopularProductsView(generics.ListAPIView):
#     queryset = Product.objects.order_by('-views')[:5]  # Получаем 5 самых популярных товаров
#     serializer_class = ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]  # Строка добавляется сюда
    filterset_fields = ['category', 'color']  # Поля, по которым будет проводиться фильтрация