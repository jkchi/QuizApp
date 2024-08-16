# import model
from .models import Quiz
from django.contrib.auth.models import User
from submissions.models import Submission
from questions.models import *

# import serializer
from .serializer import QuizSerializer, QuizListSerializer,StudentQuizSerializer,QuizCreateSerializer
from questions.serializer import QuestionSerializer


# import api doc func tool
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# import Util
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone

# all atomic db write
from django.db import transaction

# support wrong id return 404 method
# from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    
    # notice dynamic queryset 
    # the basename in url.py need to be assigned  
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Quiz.objects.all()
        else:
            return Quiz.objects.filter(is_published=True)
    
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
        elif self.action == 'create':
            return QuizCreateSerializer
        return super().get_serializer_class()
    
    @swagger_auto_schema(
    request_body= QuizCreateSerializer()  # Correct as it expects a list of questions
    )    
    def create(self, request, *args, **kwargs):
        print('func called here')
        with transaction.atomic():
            print('op started')
            response = super().create(request, *args, **kwargs)
            
            # get the quiz_id just assigned
            quiz_id = response.data['id']
            quiz = Quiz.objects.get(id=quiz_id)
            print('in here')
            # student are the non admins
            students = User.objects.filter(is_staff=False) 

            # create empty submissions for each student
            # allow dashboard edit
            submissions = [
                Submission(
                    quiz=quiz,
                    student=student,
                    score=0,
                    attendance_status=False,  
                    submitted_at=None  
                )
                for student in students
            ]

            Submission.objects.bulk_create(submissions)  

        return response
    
    @swagger_auto_schema(
    method='post',
    request_body= QuestionSerializer(many=True),  # Correct as it expects a list of questions
    responses = {
        200: QuestionSerializer(many=True, read_only=True),  
        400: 'Error response' 
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

    
    
    @swagger_auto_schema(
        method='post',
        operation_description="Validate quiz answers",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Question ID'),
                    'option': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description='Selected Options ID'
                    )
                },
                required=['id', 'option']
            )
        ),
        responses={
            200: openapi.Response(
                description="Validation results",
                examples={
                    "application/json": {
                        "score": 80,
                        "question_info": [
                            {"id": 1, "is_correct": True, "correct_option_id": [1]},
                            {"id": 2, "is_correct": False, "correct_option_id": [3, 4]}
                        ],
                        "error": []
                    }
                }
            ),
            400: openapi.Response(description="Bad Request"),
            403: openapi.Response(description="Forbidden")
        }
    )
    @action(detail=True, methods=['post'])
    def validation(self, request, pk = None): 
        user = request.user
        quiz = self.get_object()
        current_time = timezone.now()
        score = quiz.total_score
        question_count = quiz.questions.count()
        
        # check if a student has submitted the quiz
        if Submission.objects.filter(quiz=quiz, student=user).exists():
            return Response({'error': 'You have already submitted the quiz'}, status=status.HTTP_403_FORBIDDEN)
    
        # check if the quiz is submittable
        if question_count == 0:
            return Response({'error': 'No questions available in the quiz.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if quiz published
        if not quiz.is_published:
            return Response({'error': 'Quiz is not published.'}, status=status.HTTP_403_FORBIDDEN)

        # check submit time is allowed
        if not (quiz.start_time <= current_time <= quiz.end_time):
            return Response({'error': 'Current time is not within the allowed start and end time.'}, status=status.HTTP_403_FORBIDDEN)
        
        # check submit data is list
        if not (isinstance(request.data, list)):
            return Response({'error': 'The request data is not array'}, status=status.HTTP_400_BAD_REQUEST)

        # call_back_items form
        # key: question id
        # value: {is_correct : False, correct_answer_id:[]}
        call_back_items = {}
        
        call_back_error_data = []
        
        for question in quiz.questions.all():
            call_back_items[question.id] = {"is_correct" : False, "correct_option_id" : []}
            for option in question.options.all():
                if option.is_answer == True:
                    call_back_items[question.id]["correct_option_id"].append(option.id)

        # request data form
        # [id: question id , option: [selected options]]
        questions_response_data = request.data
        correct_question_count = 0
        
        for data in questions_response_data:
            qid = data.get('id')

            options = data.get('option')
            
            if qid is None or not isinstance(options, list):
                continue  
            
            if qid in call_back_items:
                correct_answer_set = set(call_back_items[qid]["correct_option_id"])
                
                # check in the inputted options is int
                try:
                    student_option_set = set(map(int, options))
                except ValueError:
                    call_back_error_data.append({'id':qid,'error': 'Invalid data format for options.'})
                    continue
                
                if correct_answer_set == student_option_set:
                    if call_back_items[qid]["is_correct"] == False:
                        correct_question_count += 1
                        call_back_items[qid]["is_correct"] = True

        call_back_question_info_data = []
        # extract qid from the call_back_items key
        # add add it to its value to form a question answer status info obj
        # and save in call_back_data to return 
        for question_id in call_back_items:
            call_back_item = call_back_items[question_id]
            call_back_item['id'] = question_id
            call_back_question_info_data.append(call_back_item)
            
        final_score = (correct_question_count / question_count) * score
        
        Submission.objects.create(
        quiz=quiz,
        student=user,
        score=final_score,
        attendance_status=True,  
        submitted_at=current_time
        )
        
        # if the api call is successful 
        # the error should be a empty string
        call_back_main = {
            'score': final_score,
            'question_info': call_back_question_info_data,
            "error" : "",
            'error_data':call_back_error_data
        }
        
        if len(call_back_error_data) > 0 :
            call_back_main["error"] = "Invalid data sent in API call"
        
        return Response(call_back_main, status=status.HTTP_200_OK)