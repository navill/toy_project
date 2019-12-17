from django.urls import include, path
from rest_framework import routers

from product import views

# router = routers.DefaultRouter()
# router.register(r'categories', views.CategoryViewSet)
# router.register(r'products', views.ProductViewSet)
# router.register(r'comments', views.CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('', include('product.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]