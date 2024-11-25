from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.profiles.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = "Create missing profiles for existing users"

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(f"Profile created for user: {user.username}")
        self.stdout.write("Finished creating missing profiles.")
