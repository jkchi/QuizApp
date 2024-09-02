from rest_framework import serializers
from .models import Quiz
from questions.serializer import QuestionSerializer,StudentQuestionSerializer

class QuizSerializer(serializers.ModelSerializer):
    
    questions = QuestionSerializer(many=True,required=False)
                                   
    class Meta:
        model = Quiz
        fields = ["id", "title","text","created_at","start_time","duration_min","end_time",'total_score','is_published','questions']


class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "title", "text", "start_time", "duration_min", "end_time", "total_score",'is_published']

class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "title", "text", "created_at", "start_time", "duration_min", "end_time", "total_score",'is_published']
        
        
class StudentQuizSerializer(serializers.ModelSerializer):
    
    # one to many relation
    questions = StudentQuestionSerializer(many=True)
                                   
    class Meta:
        model = Quiz
        fields = ["id", "title","text","created_at","start_time","duration_min","end_time",'total_score','questions']
