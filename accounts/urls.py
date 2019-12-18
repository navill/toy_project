from django.urls import path, include

"""
    accounts/login/
    accounts/logout/
    accounts/user/
    accounts/login/
    accounts/password/reset/  [required email verification]
    accounts/password/reset/confirm/  [required email verification]
    accounts/password/change/
"""
urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]
