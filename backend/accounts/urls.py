from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView,UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', UserViewSet) 

urlpatterns = [
    # just for showing different way of link a url to a view
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name = "get_token"),
    path("refresh/", TokenRefreshView.as_view(), name = "refresh"),
    # the urls which is prebulid by rest_framework including login and logout
    path("auth/", include("rest_framework.urls")),
    
    # include the router created urls
    path('', include(router.urls)),
]
