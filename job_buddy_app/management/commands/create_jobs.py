from django.core.management.base import BaseCommand 
from faker import Faker
from job_buddy_app.models import Job
from job_buddy_users.models import JobBuddyUser
from random import choice

class Command(BaseCommand):
    help = "Addings a specific count of jobs to users"

    def add_arguments(self, parser): 
        parser.add_argument('-n', '--number', type=int, help='Number of jobs to users and add them to the database')

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        all_users_objects = [user for user in JobBuddyUser.objects.all()]
        all_states = [state[0] for state in Job.STATE_CHOICES]
        all_status = [status[0] for status in Job.STATUS_CHOICES]
        
        n = kwargs['number']
        if not n:
            # Adds one by default
            n = 1 
        
        for num in range(n):
            user_choice = choice(all_users_objects)
            state_choice = choice(all_states)
            status_choice = choice(all_status)
            profile = fake.profile()

            user_instance = Job.objects.create(
                user = user_choice,
                job_name = profile['job'],
                company_name = profile['company'],
                salary = fake.random_int(min=30000, max=150000),
                job_summary = fake.paragraph(nb_sentences=6),
                job_link= fake.url(),
                job_city= fake.city(),
                status=status_choice,
                job_state = state_choice,
            )

            user_instance.save()
            print(user_instance)