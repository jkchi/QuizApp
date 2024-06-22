from rest_framework import viewsets,status
from .serializer import QuizSerializer

# import action to self define api method
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Quiz
from rest_framework.response import Response

# api doc generation schema
from drf_yasg.utils import swagger_auto_schema

from questions.serializer import QuestionSerializer
from questions.models import *




class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    
    
    # method overloaded to diy auth    
    def get_permissions(self):
        # need to be change to IsAuthenticated after testing
        if self.action == 'retrieve':
            return [AllowAny()] 
        else:
            # need to be change to IsAdminUser after testing
            return [AllowAny()]
    
    @swagger_auto_schema(
        method='post',
        request_body=QuestionSerializer(many=True),
        responses={201: QuestionSerializer(many=True)}
    )
    
    
    @action(detail=True, methods=['post'])
    def bulk_create_questions_options(self, request):        
        """
        Create multiple questions and their corresponding options for a given quiz.

        This method parses the `pk` from the URL to get the current `Quiz` object
        and then creates multiple `Question` objects associated with the `Quiz`.
        For each `Question` object, multiple `Option` objects are created.

        Expected request data format:
        [
            {
                "text": "Question 1",
                "options": [
                    {"text": "Option 1", "is_answer": false},
                    {"text": "Option 2", "is_answer": true}
                ]
            },
            {
                "text": "Question 2",
                "options": [
                    {"text": "Option 1", "is_answer": true},
                    {"text": "Option 2", "is_answer": false}
                ]
            }
        ]

        Args:
            request (Request): The HTTP request containing a list of questions
                            and their options to be created.

        Returns:
            Response: A Response object with HTTP status 201 (Created) if the questions
                    and options were successfully created.
    """
        
        # get the current object
        # this method will get the pk from url and parse it
        quiz = self.get_object()
        questions_data = request.data
        for question_data in questions_data:
            options_data = question_data.pop('options')
            question = Question.objects.create(quiz=quiz, **question_data)
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)
        return Response(status=status.HTTP_201_CREATED)

    
    # think about how to define a method
    # 1. prevent student from getting not released quiz
    # def get_questions(self, request, pk=None):