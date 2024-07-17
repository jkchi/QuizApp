from rest_framework import serializers
from .models import Quiz
from questions.serializer import QuestionSerializer

class QuizSerializer(serializers.ModelSerializer):
    
    questions = QuestionSerializer(many=True,required=False)
                                   
    class Meta:
        model = Quiz
        fields = ["id", "title","text","created_at","start_time","duration_min","end_time",'total_score','questions']

class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "title", "text", "created_at", "start_time", "duration_min", "end_time", "total_score"]
