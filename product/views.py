import django_filters
from django.db.models import Q
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view
# Function View
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.reverse import reverse

from config.permission import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from product.models import Category, Product, Comment
from product.serializers import CategorySerializer, ProductSerializer, CommentSerializer, ProductDetailSerializer, \
    CommentDetailSerializer

"""
    ProductFilter
    category: 카테고리별 필터
    name: 제품 이름 필터
    min_price & max_price: 가격 범위 필터
    date_from & date_to: 제품이 등록된 기간 필터
"""


class ProductFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.AllValuesFilter(field_name='category__name')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    date_from = django_filters.DateFilter(field_name='created', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('category', 'name', 'min_price', 'max_price', 'date_from', 'date_to')


class CommentFilter(django_filters.rest_framework.FilterSet):
    product = django_filters.AllValuesFilter(field_name='product__name')
    user = django_filters.AllValuesFilter(field_name='user__email')

    class Meta:
        model = Comment
        fields = ('product', 'user')


# ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('name', 'products')
    permission_classes = (IsAdminUserOrReadOnly,)


# API based view - Response(JsonResponse 포함)
class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_class = ProductFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAdminUserOrReadOnly,)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class CommentList(ListCreateAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CommentFilter
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    # 작성자가 아닐경우 read only, 작성자일 경우 editable
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        product = self.request.query_params.get('product')
        user = self.request.query_params.get('user')
        if product or user:
            if product and user:
                queryset = queryset.filter(Q(user__email=user) & Q(product__name=product))
            else:
                queryset = queryset.filter(Q(user__email=user) | Q(product__name=product))
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        parent_obj = None
        if request.data['parent']:
            parent_obj = Comment.objects.get(id=request.data['parent'])
        product = Product.objects.get(id=request.data['product'])
        Comment.objects.create(
            user=request.user,
            product=product,
            parent=parent_obj,
            body=request.data['body'],
        )
        return HttpResponseRedirect(reverse('product:comment-list'))


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    # filter_backends = [DjangoFilterBackend]
    # filter_class = CommentFilter
    permission_classes = (IsOwnerOrReadOnly,)


@api_view(['GET'])
def api_root(request):
    return Response({
        'categories': reverse('category-list', request=request),
        'products': reverse('product-list', request=request),
        'comments': reverse('comment-list', request=request),
    })

# class ApiRoot(generics.GenericAPIView):
#     name = 'api-root'
#
#     def get(self, request, *args, **kwargs):
#         return Response({
#             'categories': reverse('product:category-list'),
#             'products': reverse('product:product-list'),
#             'comments': reverse('product:comment-list'),
#         })
