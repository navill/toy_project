from django.contrib import admin
from django.urls import include, path

# from product.views import api_root, ApiRoot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('product.urls')),
    path('accounts/', include('accounts.urls')),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
