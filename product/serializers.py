from rest_framework import serializers

from product.models import Category, Product, Comment


# class RecursiveFields(RecursiveField):
#     def to_native(self, value):
#         return self.parent.to_native(value)

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    # # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), )
    # absolute_detail_url = serializers.SerializerMethodField()
    # # 최상위 댓글에 대한 하위 댓글 recursive
    # # reply: Comment의 child
    reply = RecursiveSerializer(many=True, read_only=True)

    # --------------------------#
    # reply = serializers.SerializerMethodField()
    comment_detail_url = serializers.SerializerMethodField()

    # url = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='comment-detail'
    # )
    class Meta:
        model = Comment
        fields = ('comment_detail_url', 'id', 'user', 'product', 'parent', 'body', 'reply')
        read_only_fields = ('id',)

    def get_comment_detail_url(self, obj):
        request = self.context['request']
        http_host = request.META['HTTP_HOST']
        path = obj.get_absolute_url()
        url = 'http://{http_host}{path}'.format(http_host=http_host, path=path)
        return url

    def get_reply(self, instance):
        print('get_reply')
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('reply', self)
        return serializer.data


class CommentDetailSerializer(serializers.ModelSerializer):
    absolute_detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('absolute_detail_url', 'id', 'user', 'product', 'parent', 'body')

    def get_absolute_detail_url(self, obj):
        request = self.context['request']
        http_host = request.META['HTTP_HOST']
        path = obj.get_absolute_url()
        url = 'http://{http_host}{path}'.format(http_host=http_host, path=path)
        return url


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    product_detail_url = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'created', 'product_detail_url', 'comment_count']

    # def get_comment_count(self, obj):
    #     comment_count = obj.comments.count()
    #     return comment_count

    def get_product_detail_url(self, obj):
        request = self.context['request']
        http_host = request.META['HTTP_HOST']
        path = obj.get_absolute_url()
        url = 'http://{http_host}{path}'.format(http_host=http_host, path=path)
        return url

    def get_comment_count(self, obj):
        queryset = Comment.objects.filter(product=obj)
        return queryset.count()


class ProductDetailSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    # comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'created', 'comment_count', 'comments']

    def get_comments(self, obj):
        result = list()
        queryset = Comment.objects.filter(product_id=obj.id, parent=None)
        for obj in queryset:
            serializer = CommentSerializer(obj, context=self.context)
            result.append(serializer.data)
        return result

    def get_comment_count(self, obj):
        queryset = Comment.objects.filter(product=obj)
        return queryset.count()


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']
        # lookup_fields = ('products',)
