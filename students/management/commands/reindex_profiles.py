from django.core.management.base import BaseCommand
from students.models import StudentProfile
from students.search import index_student_profile

class Command(BaseCommand):
    help = "Re-indexes all student profiles: builds denormalized search_corpus and BGE dense embeddings"

    def handle(self, *args, **options):
        profiles = StudentProfile.objects.select_related("user").all()
        total = profiles.count()
        self.stdout.write(f"Found {total} student profiles to index...")

        success_count = 0
        for profile in profiles:
            try:
                index_student_profile(profile)
                success_count += 1
                self.stdout.write(f"Indexed profile for: {profile.user.username}")
            except Exception as e:
                self.stderr.write(f"Failed to index {profile.user.username}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {success_count}/{total} student profiles!"))
