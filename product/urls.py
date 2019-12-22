from django.urls import path

from product import views

app_name = 'product'

category_list = views.CategoryViewSet.as_view({
    'get': 'list', 'post': 'create',
})
category_detail = views.CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
# comment_list = views.CommentViewSet.as_view({'get': 'list', 'post': 'create', })
# comment_detail = views.CommentViewSet.as_view({'get': 'retrieve',
#                                                'put': 'update',
#                                                'patch': 'partial_update',
#                                                'delete': 'destroy', })

urlpatterns = [
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>', category_detail, name='category-detail'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name='comment-detail'),
]
