from django.db import models

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

    job_name = models.CharField(max_length=80)
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




    


