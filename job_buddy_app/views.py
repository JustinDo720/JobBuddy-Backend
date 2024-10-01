from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .serializers import JobSerializer
from .models import Job

# Create your views here. 

class JobList(generics.ListCreateAPIView):
    """
        We list ALL Job Instance from our Users:
            1) This is a ListCreateAPIView, which means it allows GET and POST 
            2) We're displaying all jobs; therefore, our serializer sets `many=True`
        
    """
    queryset = Job.objects.all() 
    serializer_class = JobSerializer

    # "GET" Method
    def list(self, request):
        queryset = self.get_queryset()
        # Because we're displaying a lot of Jobs...
        serializer = JobSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class SpecificJob(generics.RetrieveAPIView):
    """
        Given an Id, we're going to retrieve a specific Job and return all the information from it.
            1) This is a normal RetrieveAPIView, which means only GET method
    """
    queryset = Job.objects.all() 
    serializer_class = JobSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
     

class UpdateJob(generics.RetrieveUpdateAPIView):

    """
        Given an ID, we retrieve the Job Instance for our users to Edit:
            1) This is a "Partial" Edit which means, we don't need the users to "re-fill" out the form just choose specific fields they want to edit
            2) Again, we're using ID for now instead of "slugs"
            3) This is a RetrieveUpdateAPIView, which means it allows GET, PUT, PATCH 
            4) Automatic Approach with queryset to use `self.get_object()`

    """

    queryset = Job.objects.all() 
    serializer_class = JobSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # Manual Approach:
        # id = kwargs.get('id')
        # Job.objects.get_object_or_404(Job, id=id)
        #
        # Automaic Approach:
        # uses the lookup_field to grab our instance to edit 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveJob(generics.RetrieveDestroyAPIView):
    """
        Given an ID, we retrieve the Job Instance for our users to Delete:
            1) This is a RetrieveDeleteAPIView, which means it allows GET and Delete
            2) We return a Message that saids the instance was removed from our records
    """
    
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object() 
        instance.delete()
        return Response({"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
       
        
        

