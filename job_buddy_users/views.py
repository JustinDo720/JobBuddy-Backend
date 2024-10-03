from django.shortcuts import render
from .models import JobBuddyUser
from .serializers import JobBuddyUserSerializer
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.

class SpecificUser(generics.RetrieveAPIView):
    queryset = JobBuddyUser.objects.all()
    serializer_class = JobBuddyUserSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()    # Basically: JobBuddyUser.objects.get(id=args[0])
        serailizer = self.get_serializer(instance, many=False)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    
