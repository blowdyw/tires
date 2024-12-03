from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product  # Импортируем модель Product

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def total_price(self):
        total = sum(item.total_price for item in self.cartitem_set.all())
        return total - self.discount

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Ссылаемся на модель Product из другого приложения
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.email}'s cart"
