from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "quiz","student","attendance_status","score","submitted_at"]

        # set the author field to be read only
        extra_kwargs = {"student":{"read_only":True}}