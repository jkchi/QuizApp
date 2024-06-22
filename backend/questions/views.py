from rest_framework import viewsets,status
from .serializer import QuestionSerializer,OptionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from .models import Question,Option
from rest_framework.response import Response

# self define api in viewset
from rest_framework.decorators import action

#api document generation 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    
    # need to be change to IsAdminUser after testing
    permission_classes = [AllowAny]
    
    
class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    
    # need to be change to IsAdminUser after testing
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'question': openapi.Schema(type=openapi.TYPE_INTEGER, description='Question ID'),
                    'text': openapi.Schema(type=openapi.TYPE_STRING, description='Option text'),
                    'is_answer': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is this the correct answer')
                },
                required=['question', 'text']
            ),
        ),
        responses={201: openapi.Response('Created', OptionSerializer(many=True))}
    )
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        Option.objects.bulk_create([Option(**item) for item in serializer.validated_data])
    