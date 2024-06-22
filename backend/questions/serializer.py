from rest_framework import serializers
from .models import Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "question", "text", "is_answer"]
        
        
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True,required=False)
    class Meta:
        model = Question
        fields = ["id", "text",'quiz',"options"]
