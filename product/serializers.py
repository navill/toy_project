from django.contrib.sites.models import Site
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated

from product.models import Category, Product, Comment


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, view_name='product-detail', read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'products', 'parent']


class CommentSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='name')
    detail_url = serializers.SerializerMethodField()
    # detail_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'parent', 'body','detail_url']

    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        data.update({'user': instance.user.email})
        return data

    # 댓글 생성 시
    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_authenticated:
            if validated_data['user']:
                validated_data.pop('user')
            validated_data['user'] = request.user
        else:
            raise NotAuthenticated("Current user is not authenticated")
        instance = Comment.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        request = self.context['request']
        if request.user.is_authenticated and request.user == validated_data['user']:
            super(CommentSerializer, self).update(instance, validated_data)
        else:
            raise NotAuthenticated("Current user and writer do not match.")
        return instance

    def get_detail_url(self, obj):
        domain = Site.objects.get_current().domain
        path = obj.get_absolute_url()
        url = 'http://{domain}{path}'.format(domain=domain, path=path)
        return url


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
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'quantity', 'created', 'comment_count', 'comments']

    def get_comment_count(self, obj):
        comment_count = obj.comments.count()
        # if obj.comments.parent:
        return comment_count
