import functools

from rest_framework import serializers

from product.models import Category, Product, Comment


def memoize(fn):
    cache = dict()
    print(cache)

    @functools.wraps(fn)
    def memoizer(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]

    return memoizer


# class RecursiveFields(RecursiveField):
#     def to_native(self, value):
#         return self.parent.to_native(value)

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), )
    absolute_detail_url = serializers.SerializerMethodField()
    # 최상위 댓글에 대한 하위 댓글 recursive
    # reply: Comment의 child
    reply = RecursiveSerializer(many=True, read_only=True)

    # reply = RecursiveFields(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'product', 'parent', 'body', 'parent', 'absolute_detail_url', 'reply')

    def get_absolute_detail_url(self, obj):
        request = self.context['request']
        http_host = request.META['HTTP_HOST']
        path = obj.get_absolute_url()
        url = 'http://{http_host}{path}'.format(http_host=http_host, path=path)
        return url


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    product_detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'created', 'product_detail_url', ]

    # def get_comment_count(self, obj):
    #     comment_count = obj.comments.count()
    #     return comment_count

    def get_product_detail_url(self, obj):
        request = self.context['request']
        http_host = request.META['HTTP_HOST']
        path = obj.get_absolute_url()
        url = 'http://{http_host}{path}'.format(http_host=http_host, path=path)
        return url


class ProductDetailSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'created', 'comments']

    @memoize
    def to_representation(self, instance):
        serializer = super(ProductDetailSerializer, self).to_representation(instance)
        return serializer


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']
        # lookup_fields = ('products',)
