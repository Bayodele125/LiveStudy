from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    # required fields for the project student info
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    major = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()

    # Optional profile picture URL
    profile_picture_url = models.URLField(blank=True, null=True)

    # Django user flags
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'student_id']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class InstructorProfile(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # e.g., 'I123'
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='instructors')
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)  # e.g., {'twitter': 'https://twitter.com/instructor'}
    profile_picture_url = models.URLField(blank=True, null=True)  # URL to the instructor's profile picture


    def __str__(self):
        return self.name
    
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)  # e.g., {'twitter': 'https://twitter.com/student'}
    profile_picture_url = models.URLField(blank=True, null=True)  # URL to the student's profile picture

    def __str__(self):
        return f'{self.user.name} Profile'