from rest_framework import viewsets
from .serializer import SubmissionSerializer
from .models import Submission
from rest_framework.permissions import IsAuthenticated,IsAdminUser
# Create your views here.
class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAdminUser]
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()] 
        elif self.action == 'retrieve':
            return [IsAuthenticated()] 
        else:
            # need to be change to IsAdminUser after testing
            return [IsAdminUser()]
    
    def get_queryset(self):
        user = self.request.user
        
        # use to disable the doc bug
        if getattr(self, 'swagger_fake_view', False):
            return Submission.objects.none()
        
        if user.is_staff:
            return Submission.objects.all()
        else:
            return Submission.objects.filter(student=user)