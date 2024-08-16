from rest_framework import viewsets
from .serializer import SubmissionSerializer
from .models import Submission
# Create your views here.
class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Submission.objects.all()
        else:
            return Submission.objects.filter(student=user)