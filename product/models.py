from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
