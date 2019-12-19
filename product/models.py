from django.db import models

from accounts.models import User


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
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parents', on_delete=models.SET_NULL, null=True, blank=True)
    body = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
