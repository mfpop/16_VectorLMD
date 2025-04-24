from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.authenticate.models import Profile


class Command(BaseCommand):
    help = "Creates missing profiles for users"

    def handle(self, *args, **options):
        count = 0
        for user in User.objects.all():
            # Check if user has a profile
            try:
                profile = user.profile
                self.stdout.write(f"User {user.username} already has a profile")
            except Profile.DoesNotExist:
                # Create profile if it doesn't exist
                Profile.objects.create(user=user)
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created profile for user {user.username}")
                )

        self.stdout.write(self.style.SUCCESS(f"Created {count} missing profiles"))
