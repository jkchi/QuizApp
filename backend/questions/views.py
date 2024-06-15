from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import QuestionSerializer,OptionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from .models import Question,Option

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    
    # need to be change to IsAdminUser after testing
    permission_classes = [AllowAny]
    
    