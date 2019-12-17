from rest_framework import serializers

from product.models import Category, Product


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, view_name='product-detail', read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'products']


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), many=True, view_name='category-list')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'quantity', 'created']
