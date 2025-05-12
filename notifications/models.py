from django.db import models

from accounts.models import CustomUser
from tickets.models import Ticket


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('ticket_created', 'Nouveau ticket créé'),
        ('ticket_assigned', 'Ticket assigné'),
        ('ticket_status_changed', 'Statut du ticket modifié'),
        ('ticket_comment', 'Nouveau commentaire'),
        ('ticket_resolved', 'Ticket résolu'),
        ('ticket_closed', 'Ticket fermé'),
    )

    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} pour {self.recipient.username}"