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
    
    user_id = models.CharField(max_length=20, unique=True, primary_key=True)

    # required fields for the project student info
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    # Optional fields for additional user information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Optional profile picture URL & major
    profile_picture_url = models.URLField(blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)

    # Django user flags
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Custom flags for student/instructor roles
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_id
    
class InstructorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='instructors')
    bio = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)  # e.g., {'twitter': 'https://twitter.com/instructor'}
    profile_picture_url = models.URLField(blank=True, null=True)  # URL to the instructor's profile picture


    def __str__(self):
        return self.user.name

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='students')
    bio = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)  # e.g., {'twitter': 'https://twitter.com/student'}
    profile_picture_url = models.URLField(blank=True, null=True)  # URL to the student's profile picture

    def __str__(self):
        return f'{self.user.name} Profile'