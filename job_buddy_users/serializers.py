from rest_framework import serializers
from .models import JobBuddyUser

class JobBuddyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobBuddyUser
        fields = '__all__'