from rest_framework import serializers
from .models import JobBuddyUser
# from job_buddy_app.serializers import JobImagesSerializer
from job_buddy_app.models import Job, JobImages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JobBuddyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobBuddyUser
        fields = '__all__'


class UserJobImagesSerializer(serializers.ModelSerializer):
    job_img_api_link = serializers.HyperlinkedIdentityField(
        view_name='individual_image_job',
        lookup_field='id'
    )

    class Meta:
        model = JobImages
        fields = (
            'id',
            'job_img',
            'job_img_api_link'

        )

class UserJobSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField
    # It would be 'job_buddy_app:specific_job' however, we didn't put the 
    # app_name = 'job_buddy_app'
    # in our job_buddy_app.urls
    job_api_link = serializers.HyperlinkedIdentityField(
        view_name='specific_job',
        lookup_field='id'
    )

    # Again make sure this matches with the reverse (related name)
    # in your JobImages Model
    job_images = UserJobImagesSerializer(many=True, read_only=True)
    def get_location(self, job_object):
        return job_object.location()
    
    class Meta:
        model = Job
        fields = (
            'id',
            'job_name',
            'job_api_link',
            'job_link',
            'job_post_date',
            'company_name',
            'salary',
            'status',
            'job_summary',
            'location',
            'job_images'

        )


class UserSpecificJobSerialzier(serializers.ModelSerializer):
    # Use this serializer to retrieve jobs for a User
    user_jobs = UserJobSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobBuddyUser
        fields = (
            'id',
            'email',
            'user_jobs'
        )

# Customized Token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add your extra responses here
        data['username'] = self.user.username
        data['user_id'] = self.user.id
        return data