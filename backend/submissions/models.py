from django.db import models
from django.utils import timezone
from quizzes.models import Quiz
from django.contrib.auth.models import User

# Create your models here.

class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    attendance_status = models.BooleanField(default=True)
    score = models.FloatField(default=0)  
    submitted_at = models.DateTimeField(default=timezone.now)  # 添加默认值

    def __str__(self) -> str:
        return f"Submission by {self.student.username} for {self.quiz.title} with score {self.score}"
