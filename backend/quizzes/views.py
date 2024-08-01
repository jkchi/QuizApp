from rest_framework import viewsets,status
from .serializer import QuizSerializer, QuizListSerializer,StudentQuizSerializer

# import action to self define api method
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Quiz
from rest_framework.response import Response

# api doc generation schema
from drf_yasg.utils import swagger_auto_schema

from questions.serializer import QuestionSerializer
from questions.models import *

# all atomic db write
from django.db import transaction

# support wrong id return 404 method
# from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist


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
        
    
    def get_serializer_class(self):
        
        # if the current user is not staff
        # return the student serializer 
        # the is_answer is not contained
        if not self.request.user.is_staff:
            return StudentQuizSerializer
        
        # else teacher is the admin
        # return the admin serializer 
        if self.action == 'list':
            return QuizListSerializer
        elif self.action == 'retrieve':
            return QuizSerializer  
        return super().get_serializer_class()
    
    @swagger_auto_schema(
    method='post',
    request_body= QuestionSerializer(many=True),  # Correct as it expects a list of questions
    responses = {
        200: QuestionSerializer(many=True, read_only=True),  # Use 200 OK for successful bulk update
        400: 'Error response'  # Describe the error response format
        }
    )    
    @action(detail=True, methods=['post'])
    def questions_options(self, request, pk = None):        

        with transaction.atomic():
            quiz = self.get_object()
            existing_question_ids = set([question.id for question in quiz.questions.all()])
            questions_data = request.data
            call_back_data = []
            errors = []
            # question_serializers used to store updated question instance
            edited_question_serializers = []
            for question_data in questions_data:
                question_data['quiz'] = quiz.id
                
                if "id" in question_data:
                    qid = question_data['id']
                    
                    if qid not in existing_question_ids:
                        errors.append(f"No question found with ID {qid}")
                    else:
                        question = Question.objects.get(id = qid)
                        # Passing this object to the serializer tells DRF that 
                        # you intend to update this existing object rather than create a new one.
                        question_serializer = QuestionSerializer(question, data=question_data)
                        # remove question id if update a question
                        existing_question_ids.discard(qid)

                else:
                    question_serializer = QuestionSerializer(data=question_data)
                
                if question_serializer.is_valid():
                    # save the updated instance and only perform update
                    # if all serializer is_valid
                    edited_question_serializers.append(question_serializer)
                    
                    # call save later
                    # question_serializer.save() 
                    # call back can not be called after access data 
                    # call_back_data.append(question_serializer.data)
                    
                else:
                    errors.append({'question id': question_data.get('id', 'N/A'), 'error': 'Invalid data provided', 'details': question_serializer.errors})

            
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                for left_question_id in existing_question_ids:
                    Question.objects.get(id=left_question_id).delete()
                    
                # only save the question instance after 
                # all serializers are valid
                # and append the serializer data to call back
                for question_serializer in edited_question_serializers:
                    question_serializer.save()
                    call_back_data.append(question_serializer.data)
                return Response(call_back_data, status=status.HTTP_200_OK)

    
    