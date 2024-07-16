from django.db import models
from django.utils import timezone

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()    
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField(help_text="The earliest time the quiz can start")
    duration_min = models.IntegerField(default=10, help_text="The duration of the quiz in minutes set by admin")
    end_time = models.DateTimeField(help_text="The latest time the quiz can be submitted")
    
    
    def __str__(self) -> str:
        # access the id attr
        return f"Qid:{self.id} Quiz: {self.title} (Start: {self.start_time}, End: {self.end_time}, Duration:{self.duration_min}) "