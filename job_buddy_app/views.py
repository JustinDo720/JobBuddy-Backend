from django.shortcuts import render, redirect
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import generics, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import JobSerializer, JobImagesSerializer, RequiredJobImagesSerializer, RequiredJobSerializer
from .models import Job, JobImages
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Mixins - We can share specific functionality 

class JobSerializerSelectorMixin:
    # Because each API View will have this `self.get_serializer` method
    # We need to check wheather or not our method is POST
    #
    # If Post then we use our RequiredJobSerializer which includes NECESSARY fields for posting 
    # If Get then we use our normal JobSerializer to provide extra information like:
    #   user url
    #   job url
    # And others....
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return RequiredJobSerializer
        return JobSerializer

class JobImgSerializerSelectorMixin:
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return RequiredJobImagesSerializer
        return JobImagesSerializer
    


# Create your views here. 

REACT_URL = 'http://localhost:3000'


@api_view(['GET'])
def home_page(request, format=None):
    return Response({
        # We use reverse() function to grab links from view_names
        # Format deals with .json files or .api files so depending on our format suffix 
        'All Job': reverse('job_list', request=request, format=format),
        'All Users': reverse('job_buddy_users:all_users', request=request, format=format),
        'Users with Jobs': reverse('job_buddy_users:all_users_job', request=request, format=format),
        'All Job Images': reverse('images_job', request=request, format=format),
        'State and Status Choices': reverse('choices', request=request, format=format),
    })

class JobList(JobSerializerSelectorMixin, generics.ListCreateAPIView):
    """
        We list ALL Job Instance from our Users:
            1) This is a ListCreateAPIView, which means it allows GET and POST 
            2) We're displaying all jobs; therefore, our serializer sets `many=True`
        
        We also have a Mixin to choose our serializer based on:
            1) Post Request --> RequiredJobSerializer 
            2) Get Request --> JobSerializer
        
    """
    # Because of our Mixin, we DON'T need a serializer_class field: serializer_class = JobSerialzier 
    queryset = Job.objects.all().order_by('-job_post_date') 
    permission_classes = [IsAuthenticatedOrReadOnly]

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
     

class UpdateJob(JobSerializerSelectorMixin, generics.RetrieveUpdateAPIView):

    """
        Given an ID, we retrieve the Job Instance for our users to Edit:
            1) This is a "Partial" Edit which means, we don't need the users to "re-fill" out the form just choose specific fields they want to edit
            2) Again, we're using ID for now instead of "slugs"
            3) This is a RetrieveUpdateAPIView, which means it allows GET, PUT, PATCH 
            4) Automatic Approach with queryset to use `self.get_object()`
        
        We also have a Mixin to choose our serializer based on:
            1) Post Request --> RequiredJobSerializer 
            2) Get Request --> JobSerializer

        This means we WON'T need a `serializer_class` field
    """

    queryset = Job.objects.all()
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
    # Since this doesn't deal with posting, we could just add in our normal JobSerializer class for Retrieving (GET request)
    serializer_class = JobSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object() 
        instance.delete()
        return Response({"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
       
        
# Job Images

# Again Post request will have a Serializer that includes only NECESSARY fields
# Get request will have additional data fields  
# So let's create and add in our Mixin
class JobImageList(JobImgSerializerSelectorMixin, generics.ListCreateAPIView):
    """
        Listing all the Job related Images from ALL users:
            1) This is a ListCreateAPIView, which means it allows GET and POST

    """
    queryset = JobImages.objects.all()
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
    

class IndJobImage(JobImgSerializerSelectorMixin, generics.RetrieveUpdateDestroyAPIView):
    """
        Individual Job Image 
        1) It's a RetrieveUpdateDestroy meaning it takes in a GET, PUT, DELETE
        1) Allows you to modify a single instance
    
    """
    queryset = JobImages.objects.all()
    lookup_field = 'id'


    def get(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, partial=True, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete() 
        return Response({"message": "Job Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# User Jobs   

class UserJobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        user_job_queryset = Job.objects.filter(user=args[0])
        serializer = self.get_serializer(user_job_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Status and State options 
class StatusStateOptions(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'status_choices': Job.STATUS_CHOICES,
            'state_choices': Job.STATE_CHOICES
        }, status=status.HTTP_200_OK)

# Djoser Redirects to React 
def redirect_activation_url(request, uid, token):
    return redirect(f'{REACT_URL}/activate/{uid}/{token}')

def redirect_password_reset_url(request, uid, token):
    return redirect(f'{REACT_URL}/password/reset/confirm/{uid}/{token}')

def redirect_username_reset_url(request, uid, token):
    return redirect(f'{REACT_URL}/username/reset/confirm/{uid}/{token}')