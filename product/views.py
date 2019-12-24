from django.db.models import Q
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse

from config.permission import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from product.filters import ProductFilter, CommentFilter, CategoryFilter
from product.models import Category, Product, Comment
from product.serializers import CategorySerializer, ProductSerializer, CommentSerializer, ProductDetailSerializer, \
    CommentDetailSerializer


# ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    """
    - ModelViewSet
        - Category에 모델에 필요한 리스트, 상세보기, 생성, 수정, 삭제
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CategoryFilter
    permission_classes = (IsAdminUserOrReadOnly,)


# API based view - Response(JsonResponse 포함)
class ProductList(ListCreateAPIView):
    """
    - ListCreateAPIView
        - 제품의 리스트 및 생성
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter
    permission_classes = (IsAdminUserOrReadOnly,)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    """
    - RetrieveUpdateDestroyAPIView
        - 제품의 상세보기, 수정, 삭제
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class CommentList(ListCreateAPIView):
    """
    - ListCreatAPIView
        - 댓글 리스트 및 댓글 생성
    """
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CommentFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

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

        product = Product.objects.get(name=request.data['product'])
        Comment.objects.create(
            user=request.user,
            product=product,
            parent=parent_obj,
            body=request.data['body'],
        )
        return HttpResponseRedirect(reverse('product:comment-list'))


class CommentDetail(RetrieveUpdateDestroyAPIView):
    """
    - RetrieveUpdateDestroyAPIView
        - 댓글의 상세보기, 수정, 삭제
    """
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CommentFilter
    # 작성자가 아닐경우 read only, 작성자일 경우 editable
    permission_classes = (IsOwnerOrReadOnly,)


@api_view(['GET'])
def api_root(request):
    return Response({
        'categories': reverse('category-list', request=request),
        'products': reverse('product-list', request=request),
        'comments': reverse('comment-list', request=request),
    })
