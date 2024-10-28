from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_name = models.CharField(max_length=100)
    generated = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    width = models.IntegerField()
    profile = models.CharField(max_length=100)
    diameter = models.CharField(max_length=100)
    speed_index = models.CharField(max_length=100)
    load_index = models.CharField(max_length=100)
    double_load_index = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products/%Y/%m/%d')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.TextField()
    #similar_products = models.ManyToManyField('self', blank=True)
    number = models.IntegerField()
    quantity = models.IntegerField()

