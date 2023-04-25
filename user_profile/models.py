import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.owner.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/user_profiles/", filename)


class UserProfile(models.Model):
    GENDER_OPTIONS = (
        ("male", "Male"),
        ("female", "Female"),
        ("others", "Others")
    )
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_data"
    )
    gender = models.CharField(
        max_length=20, choices=GENDER_OPTIONS, default="male"
    )
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    phone = models.CharField(max_length=20, blank=True)
    works_at = models.CharField(max_length=255, blank=True)
    studies_at = models.CharField(max_length=255, blank=True)
    lives_in = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to=profile_image_file_path, blank=True)
