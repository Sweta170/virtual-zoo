from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.utils import OperationalError, ProgrammingError
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except (OperationalError, ProgrammingError):
            # Database tables might not be ready yet (e.g. before migrations).
            # Skip creating Profile here; it will be created later or manually.
            pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # When saving a user, the related profile may not exist yet during
    # initial migrations. Guard against DB errors to avoid crashing commands
    # like `createsuperuser` before migrations are applied.
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except (OperationalError, ProgrammingError):
        pass
