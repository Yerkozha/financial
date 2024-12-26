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



class Author(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

class Genre(models.Model):

    GENRE_CHOICES = (
        ('historical', 'Historical'),
        ('literature', 'Literature'),
        ('science', 'Science'),
        ('poetry', 'Poetry'),
    )
    name = models.CharField(max_length=255, choices=GENRE_CHOICES, default='literature')

class Book(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    published_date = models.DateField(blank=True, null=True)
    uploaded_by = models.ForeignKey(IndividualModel, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    book_file = models.FileField(upload_to='books/', blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    content = models.TextField()

    annotations = models.JSONField(default=dict)


class Paragraph(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="paragraphs")
    order = models.PositiveIntegerField()
    text = models.TextField()  # Raw paragraph content




class AIInsights(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="ai_insights")
    summary = models.TextField(blank=True, null=True)
    sentiment = models.JSONField(blank=True, null=True)  # Example: {"positive": 0.8, "neutral": 0.2, "negative": 0.0}
    keywords = models.JSONField(blank=True, null=True)  # Example: ["keyword1", "keyword2"]

class ProcessedContent(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="processed_content")
    tokenized = models.JSONField(blank=True, null=True)  # Tokenized text
    embeddings = models.JSONField(blank=True, null=True)  # Embedding vectors

class BookMetadata(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    metadata = models.JSONField()  # Additional metadata, e.g., publication year, language, etc.



class Favorite(models.Model):
    user = models.ForeignKey(IndividualModel, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by')
    added_date = models.DateTimeField(auto_now_add=True)






