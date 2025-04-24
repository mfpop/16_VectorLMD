"""
Script to create and apply migrations for the Profile model
Run this script from the project root directory:
python create_profile_table.py
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VectorLMD.settings")
django.setup()


def make_and_apply_migrations():
    """Create and apply migrations for the authenticate app"""
    from django.core.management import call_command

    print("Creating migrations for the authenticate app...")
    call_command("makemigrations", "authenticate")

    print("Applying migrations...")
    call_command("migrate")

    print("Creating initial Profile entries for existing users...")
    # Create profiles for any existing users that don't have one
    from django.contrib.auth.models import User
    from apps.authenticate.models import Profile

    for user in User.objects.all():
        try:
            # Check if profile exists
            profile = user.profile
        except:
            # Create profile if it doesn't exist
            print(f"Creating profile for user: {user.username}")
            Profile.objects.create(user=user)

    print("Migrations applied successfully!")


if __name__ == "__main__":
    make_and_apply_migrations()
