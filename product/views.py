from django.http import JsonResponse, HttpResponse, Http404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
# Function View
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer


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

# ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# API based view - Response(JsonResponse 포함)
class ProductList(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # list
    def get(self, request):
        categories = Product.objects.all()  # snippet queryset
        serializer = ProductSerializer(categories, many=True)
        return Response(serializer.data)

    # create
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DeosNotExist:
            raise Http404

    # retrieve
    def get(self, request, pk):
        product = self.get_object(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # update
    def put(self, request, pk):
        product = self.get_object(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # destroy
    def delete(self, request, pk):
        product = self.get_object(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def api_root(request):
    return Response({
        'categories': reverse('category-list', request=request),
        'products': reverse('product-list', request=request),
    })
