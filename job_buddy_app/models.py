from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from job_buddy_users.models import JobBuddyUser
import os 
from django.core.files import File

# # Create your models here.
class Job(models.Model):
    """
    Here's an example of our job object 
        { 
            job_name: 'Software Engineer', 
            company_name: 'Google', 
            salary: '', 
            status: 'Applied', 
            link: 'https://google.com/careers/software-engineer', 
            location: 'Mountain View, CA', 
            job_summary: 'Develop and maintain software applications.' 
        },
    """
    # Status Choices for our Choice field 
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected')
    ]

    # State choices
    STATE_CHOICES = [
        ('emp', ' '),
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    ]

    # We need an owner for this job --> One User could have multiple job posts so... let's use foreign keys
    # This will have a related_name of user_jobs for my UserJobSerializer 
    # which uses this Job Model for a Reverse
    user = models.ForeignKey(JobBuddyUser, related_name='user_jobs', on_delete=models.CASCADE)
    job_name = models.CharField(max_length=80)
    job_city = models.CharField(max_length=80)
    job_state = models.CharField(max_length=90, choices=STATE_CHOICES, default='emp')
    job_post_date = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=80)
    salary = models.IntegerField(blank=True, null=True)
    job_link = models.URLField(blank=True, null=True)
    job_summary = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=35, choices=STATUS_CHOICES, default='applied')

    def __str__(self):
        return f'{self.job_name} @ {self.company_name} - {self.status}'
    
    def location(self):
        return f'{self.job_city.title()}, {self.job_state.upper()}'


    @classmethod
    def get_status_choices(cls):
        # We're getting the initial value in the tuple because when we post
        # we're posting with this set of values
        return [{'submit_name':stat[0], 'name': stat[1]} for stat in cls.STATUS_CHOICES]
    
    @classmethod
    def get_state_choices(cls):
        return [{'submit_name':state[0],'name': state[1]} for state in cls.STATE_CHOICES]


class JobImages(models.Model):
    job = models.ForeignKey(Job, related_name='job_images', on_delete=models.CASCADE)
    job_img = models.ImageField(upload_to='job_img/')
    job_img_resized = models.ImageField(upload_to='job_img_resized/', blank=True, null=True)

    def make_resize_image(self, img, width=500, height=500):
        # We need to open the image 
        image = Image.open(img)

        # Resizing our image
        image = image.resize((width,height))

        # Saving our image in memory so it would be used as a resized image 
        img_io = BytesIO()
        image.save(img_io, format='png', quality=85)

        # Construct a File object 
        resized_img_file = File(img_io, name=img.name)
        return resized_img_file
    
    def get_resize_image(self):
        if self.job_img_resized:  # if theres a resized version already then we could set the resized name
            resized_name = self.job_img_resized.name.split('/')[-1]

        # Checking if we have a resized image already then we return its url
        # The url looks something like: [https,'', storage, app, job_img, img_name]
        if self.job_img_resized and resized_name == self.job_img.url.split('/')[-1]:
            return self.job_img_resized.url
        else:
            if self.job_img:
                # Our function make_resize_image will use pillow etc to resize
                self.job_img_resized = self.make_resize_image(self.job_img)
                self.save()

                return self.job_img_resized.url
            else:
                return ''
        
    
