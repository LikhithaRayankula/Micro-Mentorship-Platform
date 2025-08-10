from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group, Permission
from django.db import models


class User(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    class Meta:
        swappable = 'AUTH_USER_MODEL'  # Important to allow Django to swap default


class MentorUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class MentorUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name='mentoruser_set',  # ⚠️ custom related_name
        blank=True,
        help_text='The groups this mentor belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='mentoruser_permissions_set',  # ⚠️ custom related_name
        blank=True,
        help_text='Specific permissions for this mentor.',
        verbose_name='user permissions'
    )

    objects = MentorUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email





class Mentor(models.Model):
    mentor_user = models.OneToOneField('MentorUser', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default='Mentor Name')
    photo = models.ImageField(upload_to='mentor_photos/')
    qualification = models.CharField(max_length=255)
    job_role = models.CharField(max_length=255)
    about = models.TextField()
    is_paid = models.BooleanField(default=False)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Availability(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='availabilities')
    start = models.DateTimeField()
    end = models.DateTimeField()

class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    paid = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)


