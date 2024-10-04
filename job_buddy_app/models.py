from django.db import models
from job_buddy_users.models import JobBuddyUser

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

    # We need an owner for this job --> One User could have multiple job posts so... let's use foreign keys
    # This will have a related_name of user_jobs for my UserJobSerializer 
    # which uses this Job Model for a Reverse
    user = models.ForeignKey(JobBuddyUser, related_name='user_jobs', on_delete=models.CASCADE)
    job_name = models.CharField(max_length=80)
    job_post_date = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=80)
    salary = models.IntegerField()
    status = models.CharField(max_length=35, choices=STATUS_CHOICES, default='applied')

    def __str__(self):
        return f'{self.job_name} @ {self.company_name} - {self.status}'
        
    @classmethod
    def get_status_choices(cls):
        # We're getting the initial value in the tuple because when we post
        # we're posting with this set of values
        return [stat[0] for stat in cls.STATUS_CHOICES]


class JobImages(models.Model):
    job = models.ForeignKey(Job, related_name='job_images', on_delete=models.CASCADE)
    job_img = models.ImageField(upload_to='job_img/')