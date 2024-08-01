from rest_framework import serializers
from .models import Question, Option
from quizzes.models import Quiz

class OptionSerializer(serializers.ModelSerializer):
    # notice if use patch method
    # the the id in request will be used as primary key(not the one in url)
    id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Option
        # only remove question in Serializer not in models
        # so the api call will allow binding unsaved question
        # during creating question and option in the same time
        fields = ["id", "text", "is_answer"]
        
        
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True,required=False)
    
    # add quiz id to be null 
    # when quiz_{quiz_id}_questions_options use QuestionSerializer
    # since that method belong to a quiz instance
    # the quiz id no longer need to be specified  
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), required = False)
    class Meta:
        model = Question
        # remove quiz for the same reason
        fields = ["id", "text","options", 'quiz']
    
    # override the create method to allow create option with questions
    # since the cascade setting, we assume when create a question
    # there is no existing option bind to the question
    # so we cal the create method of question
    def create(self, validated_data):
        
        options_data = validated_data.pop('options', [])
        # create Question to avoid option not bounded
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    # the update should only be call if a question object exist
    # however it does not assume the the options status
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        existing_option_ids = set([option.id for option in instance.options.all()])

        options = validated_data.get('options', [])
        
        for option_data in options:
            option_id = option_data.get('id', None)
            if option_id:
                option = Option.objects.get(id=option_id, question=instance)
                option.text = option_data.get('text', option.text)
                option.is_answer = option_data.get('is_answer', option.is_answer)
                option.save()
                existing_option_ids.discard(option_id)
            else:
                Option.objects.create(question=instance, **option_data)

        for left_option_id in existing_option_ids:
            Option.objects.get(id=left_option_id).delete()
        return instance


class StudentOptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Option
        fields = ["id", "text"]

class StudentQuestionSerializer(serializers.ModelSerializer):
    options = StudentOptionSerializer(many = True)
    
    class Meta:
        model = Question
        # not include quiz id
        # since this StudentQuestionSerializer is only used in get
        fields = ["id", "text","options"]


class ValidateOptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Option
        fields = ["id"]

class ValidateQuestionSerializer(serializers.ModelSerializer):
    options = StudentOptionSerializer(many = False)
    
    class Meta:
        model = Question
        # not include quiz id
        # since this StudentQuestionSerializer is only used in get
        fields = ["id"]
        