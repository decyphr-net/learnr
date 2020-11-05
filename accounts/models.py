from django.db import models
from django.contrib.auth.models import User
from language.models import Language
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """User profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_language = models.ForeignKey(
        Language,
        related_name="first_language",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    new_language = models.ForeignKey(
        Language,
        related_name="new_language",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()