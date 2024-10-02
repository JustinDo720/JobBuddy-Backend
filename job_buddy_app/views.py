from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .serializers import JobSerializer, JobImagesSerializer
from .models import Job, JobImages
from rest_framework.parsers import MultiPartParser, FormParser

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
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
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
       
        
# Job Images

class JobImageList(generics.ListCreateAPIView):
    """
        Listing all the Job related Images from ALL users:
            1) This is a ListCreateAPIView, which means it allows GET and POST

    """
    queryset = JobImages.objects.all()
    serializer_class = JobImagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        # Because we supplied "queryset", we could retrieve this the automatic way
        # Note: self.get_object() --> will need a supplied primary key so you would use "lookup_field"
        # 
        # Therefore, we need to run self.get_queryset() to grab multiple results instead of one specific result
        instances = self.get_queryset()
        # Because we supplied "serializer_class", we could retrieve this the automatic way
        serializer = self.get_serializer(instances, many=True, context={'request': request})   # We're override many=True because we have a lot of instances
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # We need to override the create option because we're dealing with files 
    def create(self, request, *args, **kwargs):
        # We don't need to supply `files=request.FILES`` here because we're using `self.get_serializer()`
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class IndJobImage(generics.RetrieveUpdateDestroyAPIView):
    """
        Individual Job Image 
        1) It's a RetrieveUpdateDestroy meaning it takes in a GET, PUT, DELETE
        1) Allows you to modify a single instance
    
    """
    queryset = JobImages.objects.all()
    serializer_class = JobImagesSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete() 
        return Response({"message": "Job Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)