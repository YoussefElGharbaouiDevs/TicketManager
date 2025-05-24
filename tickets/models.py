from django.db import models
from model_utils import FieldTracker

from accounts.models import CustomUser


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)  # for display order
    color = models.CharField(max_length=7, blank=True, null=True)  # e.g. '#FF0000'

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=0)  # lower = lower priority

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    attached_files = models.FileField(upload_to='tickets/', blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tracker = FieldTracker(fields=['status_id'])

    class Meta:
        ordering = ['-created_at', '-updated_at', ]

    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.ticket.title}"