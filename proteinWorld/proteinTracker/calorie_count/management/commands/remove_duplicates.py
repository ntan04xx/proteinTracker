from django.core.management.base import BaseCommand
from django.db.models import Count
from django.contrib.auth.models import User
from calorie_count.models import UserDetails

class Command(BaseCommand):
    help = 'Remove duplicate UserDetails entries'

    def handle(self, *args, **kwargs):
        duplicates = UserDetails.objects.values('user__username').annotate(count=Count('user__username')).filter(count__gt=1)
        for duplicate in duplicates:
            username = duplicate['user__username']
            user_details = UserDetails.objects.filter(user__username=username).order_by('-timestamp')
            # Keep the most recent UserDetails and delete the older ones
            for detail in user_details[1:]:
                self.stdout.write(f'Deleting UserDetails for user {username}')
                detail.delete()
        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate UserDetails entries'))