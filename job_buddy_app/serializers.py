from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    status_options = serializers.SerializerMethodField()

    # Because we're following the naming convention: get_<serializer_method_field>
    # We won't need to provide a "method_name" for status_options 
    def get_status_options(self, job_obj):
        return job_obj.get_status_choices()

    class Meta:
        model = Job
        fields = (
            'id',
            'job_name',
            'company_name',
            'salary',
            'status',
            'status_options',
        )


