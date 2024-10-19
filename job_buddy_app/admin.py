from django.contrib import admin
from job_buddy_users.models import JobBuddyUser
from job_buddy_app.models import Job
# from django.contrib.auth.models import User

# Register your models here.

admin.site.register(JobBuddyUser)
admin.site.register(Job)
