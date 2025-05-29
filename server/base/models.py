from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_hr = models.BooleanField(default=False)
    resume = models.FileField(upload_to='static/resumes', null = True)
    full_name = models.CharField(max_length=255, null = True)  # NOT NULL by default
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    years_experience = models.IntegerField(blank=True, null=True)
    education_list = models.JSONField(null = True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

class SkillSets(models.Model):
    username = models.CharField(primary_key=True, max_length=150)
    skills = models.JSONField()

    def __str__(self):
        return self.username


class Education(models.Model):
    username = models.CharField(max_length=150)
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year = models.IntegerField()
    gpa = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.username
    




