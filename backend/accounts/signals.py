from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from submissions.models import Submission
from quizzes.models import Quiz

User = get_user_model()

# create empty submission for new registered user
# when some quizzes are published
@receiver(post_save, sender=User)
def create_submissions_for_new_user(sender, instance, created, **kwargs):
    if created:
        quizzes = Quiz.objects.all()

        submissions = [
            Submission(
                quiz=quiz,
                student=instance,
                score=0,
                attendance_status=False,
                submitted_at=None
            )
            for quiz in quizzes
        ]
        
        Submission.objects.bulk_create(submissions)
