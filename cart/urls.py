from django.urls import path
from .views import CartViewSet

urlpatterns = [
    path('api/carts/', CartViewSet.as_view({'get': 'list'}), name='cart-list'),
    path('api/carts/add-item/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
    path('api/carts/apply-discount/', CartViewSet.as_view({'post': 'apply_discount'}), name='cart-apply-discount'),
]
