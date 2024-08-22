from django.contrib.auth.models import User
from rest_framework import generics
from .serializer import UserSerializer
from rest_framework.permissions import AllowAny

class CreateUserView(generics.CreateAPIView):
    # create a create view inherent from the rest framework CreateAPIView
    
    # define what model this view should be operate on
    queryset = User.objects.all()

    # define the serializer, which is the must 
    # the serialize define the data model and other behaviors
    serializer_class = UserSerializer

    # define the permission of the view, and it is open to all the people
    permission_classes = [AllowAny]