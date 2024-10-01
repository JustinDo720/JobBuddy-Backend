from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    status_options = serializers.SerializerMethodField()
    # We're using IdentityField because it helps us create a url for itself rather than a another model
    job_link = serializers.HyperlinkedIdentityField(
        view_name='specific_job',
        lookup_field='id'
    )

    # Because we're following the naming convention: get_<serializer_method_field>
    # We won't need to provide a "method_name" for status_options 
    def get_status_options(self, job_obj):
        return job_obj.get_status_choices()

    class Meta:
        model = Job
        fields = (
            'id',
            'job_name',
            'job_link',
            'company_name',
            'salary',
            'status',
            'status_options',
        )


