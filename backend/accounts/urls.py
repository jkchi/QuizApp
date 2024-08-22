from django.contrib import admin
from django.urls import path,include
from .views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # just for showing different way of link a url to a view
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name = "get_token"),
    path("refresh/", TokenRefreshView.as_view(), name = "refresh"),
    # the urls which is pre bulid by rest_framework including login and logout
    path("auth/", include("rest_framework.urls")),
]
