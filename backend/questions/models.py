from django.db import models
from quizzes.models import Quiz
# Create your models here.

class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name = 'questions')

    # def __str__(self) -> str:
    #     return self.text
    def __str__(self) -> str:
        # access the id attr
        return f"ID:{self.id} Quiz ID: {self.quiz.id} text: {self.text} "

    
class Option(models.Model):
    text = models.CharField(max_length=255)
    # question to option : one to many
    # id will be added as a instance attr, so the col should be named question
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name = 'options')
    is_answer = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        # access the id attr
        return f"ID:{self.id} Question ID: {self.question.id} text: {self.text} is_answer: {self.is_answer}"
