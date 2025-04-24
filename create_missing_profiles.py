"""
Script to create missing Profile objects for existing users
Run this script from the project directory:
python create_missing_profiles.py
"""

import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a.settings")
django.setup()


def create_missing_profiles():
    from django.contrib.auth.models import User
    from apps.authenticate.models import Profile

    count = 0
    for user in User.objects.all():
        try:
            # Check if profile exists - access the attribute without assigning to variable
            user.profile
            print(f"User {user.username} already has a profile")
        except Profile.DoesNotExist:  # Use specific exception
            # Create profile if it doesn't exist
            Profile.objects.create(user=user)
            count += 1
            print(f"Created profile for user {user.username}")

    print(f"Created {count} missing profiles")


if __name__ == "__main__":
    create_missing_profiles()
