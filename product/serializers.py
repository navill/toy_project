from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from accounts.models import User
from product.models import Category, Product, Comment


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, view_name='product-detail', read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'products']


#
# #
class CommentSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='name')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'parent', 'body']


# class CommentSerializer(serializers.HyperlinkedModelSerializer):
#     product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='name')
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'product', 'parent', 'body']
#
#     def to_representation(self, instance):
#         data = super(CommentSerializer, self).to_representation(instance)
#         print(instance)
#         if data['parent'] is not None:
#             print(data)
#         # data.update({'parent': 1123})
#         return data


class ProductSerializer(WritableNestedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'quantity', 'created', 'comments']
