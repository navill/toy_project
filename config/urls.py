from django.urls import include, path

urlpatterns = [
    path('shop/', include('product.urls')),
    path('accounts/', include('accounts.urls')),

    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
