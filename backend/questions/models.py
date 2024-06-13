from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Question(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text
    
class Option(models.Model):
    text = models.TextField()
    # question to option : one to many
    # id will be added as a instance attr, so the col should be named question
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name = 'options')
    is_answer = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        # access the id attr
        return f"Qid:{self.question.id} text:{self.text} is_answer{self.is_answer}"
