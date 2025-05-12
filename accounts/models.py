from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('agent', 'Agent de support'),
        ('client', 'Client'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    categories = models.ManyToManyField('tickets.Category', blank=True, related_name='agents')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
