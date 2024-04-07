import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import CustomUserManager
# class RolesModel(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#
#     def __str__(self):
#         return self.name


class IndividualModel(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    MANAGER = 2
    CLIENT = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (CLIENT, 'Client')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid  = models.UUIDField(unique=True, editable=True, default=uuid.uuid4, verbose_name='Public Identifier')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    create_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

'''
    start: date time
    end: date time
    title: string
    summary: string
    color: string
'''


class AppointmentModel(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(IndividualModel, on_delete=models.CASCADE, related_name='appointments')

    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    title = models.CharField(max_length=255, default='new event')
    summary = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)

    create_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}Appointment for {self.user.email} on {self.start}"


class DeviceToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(IndividualModel, on_delete=models.CASCADE, related_name='device_token')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token



class PushNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)




class ErrorFeedback(models.Model):
    
    description = models.TextField()
    
    user = models.ForeignKey(IndividualModel, on_delete=models.CASCADE, related_name='feedback')
    
    def __str__(self):
        return f"{self.user.email}"


