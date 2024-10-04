from rest_framework import serializers
from .models import JobBuddyUser
from job_buddy_app.serializers import RequiredJobSerializer


class JobBuddyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobBuddyUser
        fields = '__all__'

class UserSpecificJobSerialzier(serializers.ModelSerializer):
    # Use this serializer to retrieve jobs for a User
    user_jobs = RequiredJobSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobBuddyUser
        fields = (
            'email',
            'user_jobs'
        )