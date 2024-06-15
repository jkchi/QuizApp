from rest_framework import serializers
from .models import Question, Option

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text",'quiz']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "question", "text", "is_answer"]
