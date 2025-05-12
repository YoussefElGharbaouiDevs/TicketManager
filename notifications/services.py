from .models import Notification


def create_notification(recipient, ticket, notification_type, message=None):
    """
    Crée une notification pour un utilisateur.
    """
    if message is None:
        # Messages par défaut selon le type
        messages = {
            'ticket_created': f"Nouveau ticket créé: {ticket.title}",
            'ticket_assigned': f"Vous avez été assigné au ticket: {ticket.title}",
            'ticket_status_changed': f"Le statut du ticket {ticket.title} a été mis à jour",
            'ticket_comment': f"Nouveau commentaire sur le ticket: {ticket.title}",
            'ticket_resolved': f"Le ticket {ticket.title} a été marqué comme résolu",
            'ticket_closed': f"Le ticket {ticket.title} a été fermé",
        }
        message = messages.get(notification_type, "Nouvelle mise à jour sur votre ticket")

    return Notification.objects.create(
        recipient=recipient,
        ticket=ticket,
        notification_type=notification_type,
        message=message
    )