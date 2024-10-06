# Must import the commands class so we add in some additional features
from django.core.management.base import BaseCommand 
from job_buddy_users.models import JobBuddyUser
from faker import Faker


class Command(BaseCommand):
    help = "Addings a specific count of users given"

    def add_arguments(self, parser): 
        parser.add_argument('-n', '--number', type=int, help='Number of users to add to the database')

    def handle(self, *args, **kwargs):
        fake = Faker()

        n = kwargs['number']
        if not n:
            # Adds one by default
            n = 1 
        

        for num in range(n):
            f_name = fake.first_name()
            f_name2 = fake.language_name()

            info = {
                'username': f'{f_name} {f_name2}', 
                'email':  f'{f_name}_{f_name2}@{fake.domain_name()}'
            }
            info['password'] = f'{info['username'].split(' ')[0]}123'
            user_instance = JobBuddyUser.objects.create(
                username=info['username'],
                password=info['password'],
                email=info['email']
            )
            user_instance.save()

        