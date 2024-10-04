from rest_framework import serializers
from .models import Job, JobImages



class JobImagesSerializer(serializers.ModelSerializer):
    job_name = serializers.SerializerMethodField()
    # Here we use Related Field instead of Identity because we're referring to another Model
    # So we just point it to a view that showcases an indiviudal job information 
    job_url = serializers.HyperlinkedRelatedField(
        view_name='specific_job',
        lookup_field='id',
        read_only=True,
        source='job'    # We chose job because in our fields, this points to our ForienKey
    )

    
    # Here, we're pointing to our own image link
    # So we could view this image object individually
    job_img_link = serializers.HyperlinkedIdentityField(
        view_name='individual_image_job',
        lookup_field='id',
    )

    # Naming convention get_<serializer_method_field_name>
    def get_job_name(self, job_instance):
        return job_instance.job.job_name

    class Meta:
        model = JobImages
        fields = (
            'id',
            'job',
            'job_name',
            'job_url',
            'job_img',
            'job_img_link',
        )


class JobSerializer(serializers.ModelSerializer):

    status_options = serializers.SerializerMethodField()
    # We're using IdentityField because it helps us create a url for itself rather than a another model
    job_link = serializers.HyperlinkedIdentityField(
        view_name='specific_job',
        lookup_field='id'
    )
    user_link = serializers.HyperlinkedRelatedField(
        view_name='job_buddy_users:specific_user',
        lookup_field='id', 
        read_only=True,
        source='user'
    )
    # Because we're using 'job_images' there must be a REVERSE because your Job Model doesn't automatically have the field "job_names"
    # So we make sure we update our model to:
    # job = models.ForeignKey(Job, related_name='job_images', on_delete=models.CASCADE)
    #
    # Where Related names is exactly job_images
    job_images = JobImagesSerializer(many=True, read_only=True)

    # Because we're following the naming convention: get_<serializer_method_field>
    # We won't need to provide a "method_name" for status_options 
    def get_status_options(self, job_obj):
        return job_obj.get_status_choices()

    class Meta:
        model = Job
        fields = (
            'id',
            'user',
            'user_link',
            'job_name',
            'job_link',
            'company_name',
            'salary',
            'status',
            'status_options',
            'job_images',
        )

# Required Fields for Job Serializers.
# We could use this for POSTING because there are no unnecessary fields
class RequiredJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"