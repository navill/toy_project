from django.urls import path, include

# from accounts.views import UserProfileView

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
    # path('user_profile/<int:pk>', UserProfileView.as_view()),
]
