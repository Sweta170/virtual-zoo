from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a zookeeper user with the specified username and password'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        
        # Create user and set password
        user = User.objects.create_user(username=username, password=password)
        
        # Set role to zookeeper
        user.profile.role = 'zookeeper'
        user.profile.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created zookeeper user: {username}')
        )