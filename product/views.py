import django_filters
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
# Function View
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.reverse import reverse

from config.permission import IsAdminUserOrReadOnly
from product.models import Category, Product, Comment
from product.serializers import CategorySerializer, ProductSerializer, CommentSerializer, ProductDetailSerializer

# # function based view - return JsonResponse
# # function based view는 browsable API를 자동으로 제공하지 않는다.
# @api_view(['GET', 'POST'])
# def category_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()  # snippet queryset
#         serializer = CategorySerializer(categories, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         # @api_view에서 parsing을 포함한다.
#         # data = JSONParser().parse(request)  # python 객체로 변환
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return JsonResponse(serializer.data)
#     elif request.method == 'PUT':
#         # data = JSONParser().parse(request)
#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         category.delete()
#         return HttpResponse(status=204)


"""
    ProductFilter
    category: 카테고리별 필터
    name: 제품 이름 필터
    min_price & max_price: 가격 범위 필터
    date_from & date_to: 제품이 등록된 기간 필터
"""


# class CategoryTreeFilter(django_filters.AllValuesFilter):
#     pass


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
    reply = django_filters.AllValuesFilter(field_name='parent')


# ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_fields = ('name', 'products')
    permission_classes = (IsAdminUserOrReadOnly,)


# API based view - Response(JsonResponse 포함)
class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_class = ProductFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAdminUserOrReadOnly,)

    # list
    # def get(self, request):
    #     products = Product.objects.defer('comments')
    #     # hyperlinked relation에서는 반드시 serializing 과정에서 context를 포함해야한다.
    #     # viewset은 자동 처리
    #     serializer = ProductSerializer(products, many=True, context={'request': request})
    #     return Response(serializer.data)
    #
    # # create
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    # def get_object(self, pk):
    #     try:
    #         return Product.objects.get(pk=pk)
    #     except Product.DeosNotExist:
    #         raise Http404
    #
    # # retrieve
    # def get(self, request, pk):
    #     product = self.get_object(pk=pk)
    #     serializer = ProductDetailSerializer(product, context={'request': request})
    #     return Response(serializer.data)
    #
    # # update
    # def put(self, request, pk):
    #     product = self.get_object(pk=pk)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # destroy
    # def delete(self, request, pk):
    #     product = self.get_object(pk=pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CommentFilter

    # 작성자가 아닐경우 read only, 작성자일 경우 editable
    # permission_classes = (IsOwnerOrReadOnly,)

    @action(methods=['get', 'post'], detail=True)
    def list(self, request, *args, **kwargs):
        # 최상위 댓글(reply가 null)
        queryset = Comment.objects.filter(parent=None)
        for query in queryset:
            print(query)
        # queryset = Comment.objects.all()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_root(request):
    return Response({
        'categories': reverse('category-list', request=request),
        'products': reverse('product-list', request=request),
        'comments': reverse('comment-list', request=request),
    })
