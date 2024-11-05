from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductCreateView,
    FavoriteListCreateView,
    ProductDetailView  # Импортируйте новое представление для получения продукта по ID
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),  # Получение списка категорий
    path('all/', ProductListView.as_view(), name='product-list'),  # Получение списка продуктов
    path('create/', ProductCreateView.as_view(), name='product-create'),  # Создание нового продукта
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Получение продукта по ID
    path('favorite/', FavoriteListCreateView.as_view(), name='favorite-create'),  # Используйте .as_view()
]
