from django.shortcuts import render
from .models import JobBuddyUser
from .serializers import JobBuddyUserSerializer, UserSpecificJobSerialzier
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.

class JobUsers(generics.ListAPIView):
    """
        Lists all users in our database:
            1) Because we have Djoser, we don't need this to be a ListCreateAPIView
            2) Simply lists out all users that exists in our Database
    """
    queryset = JobBuddyUser.objects.all()
    serializer_class = JobBuddyUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SpecificUser(generics.RetrieveAPIView):
    queryset = JobBuddyUser.objects.all()
    serializer_class = JobBuddyUserSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()    # Basically: JobBuddyUser.objects.get(id=args[0])
        serailizer = self.get_serializer(instance, many=False)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    
class UserSpecificJobs(generics.ListAPIView):
    """
        Lists all users in our database HOWEVER:
            1) These users come with their respected Job List
            2) Returns a list of users with their job posting
    """
    queryset = JobBuddyUser.objects.all()
    serializer_class = UserSpecificJobSerialzier

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
