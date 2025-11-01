# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify


# ==============================
# Custom User
# ==============================
class User(AbstractUser):
    """
    Custom user model for CampusConnect.
    Extends Django's default user with role and profile info.
    """
    is_talent_finder = models.BooleanField(default=False)
    is_talent_seeker = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=512, blank=True, help_text='Comma separated skills')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.username or self.email


# ==============================
# Seeker Models
# ==============================
class Interest(models.Model):
    """Normalized interests for Talent Seekers."""
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SeekerProfile(models.Model):
    """Profile for Talent Seekers."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seeker_profile')
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    university = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    interests = models.ManyToManyField(Interest, blank=True, related_name='seekers')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def interests_list(self):
        return ", ".join([i.name for i in self.interests.all()])

    def __str__(self):
        return f"SeekerProfile({self.user.username})"


# ==============================
# Finder Models
# ==============================
class OpportunityType(models.Model):
    """Types of opportunities a Finder can offer."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FinderProfile(models.Model):
    """Profile for Talent Finders."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finder_profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    university = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    opportunities = models.ManyToManyField(OpportunityType, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FinderProfile({self.user.username})"
