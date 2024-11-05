from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

class Favorite(models.Model):
    # Пользователь, который добавил продукт в избранное
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Продукт, добавленный в избранное
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="favorited_by")
    # Дата и время добавления продукта в избранное
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Возвращает строковое представление избранного продукта с указанием пользователя и названия продукта
        return f"{self.user.email} - {self.product.main_name}"

class Category(models.Model):
    # Название категории (например, "Шины", "Диски" и т.д.)
    name = models.CharField(max_length=100)

    def __str__(self):
        # Возвращает имя категории для удобного отображения
        return self.name
class Product(models.Model):
    # Other fields...
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    main_name = models.CharField(max_length=100)
    generated = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    width = models.IntegerField(validators=[MinValueValidator(0)])
    profile = models.CharField(max_length=100)
    diameter = models.CharField(max_length=100)
    speed_index = models.CharField(max_length=100)
    load_index = models.CharField(max_length=100)
    double_load_index = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.TextField()
    similar_products = models.ManyToManyField('self', blank=True)
    number = models.IntegerField(validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    # Remove the views field
    # views = models.IntegerField(default=0)  # Removed this line

    def __str__(self):
        return f"{self.main_name} - {self.model}"

