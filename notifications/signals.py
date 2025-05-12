from django.db.models.signals import post_save
from django.dispatch import receiver
from tickets.models import Ticket, Status
from .services import create_notification


@receiver(post_save, sender=Ticket)
def notify_ticket_changes(sender, instance, created, **kwargs):
    """
    Envoie des notifications lorsqu'un ticket est créé ou modifié.
    """
    if created:
        # # Notifier l'admin de la création d'un ticket
        # for admin in instance.created_by.get_admins():
        #     create_notification(admin, instance, 'ticket_created')

        # Notifier l'agent assigné
        if instance.assigned_to:
            create_notification(instance.assigned_to, instance, 'ticket_assigned')
    else:
        # Vérifier les changements de statut
        if instance.tracker.has_changed('status_id'):
            old_status_id = instance.tracker.previous('status_id')
            old_status = Status.objects.get(id=old_status_id).name if old_status_id else "Inconnu"

            # Notifier le client du changement de statut
            create_notification(instance.created_by, instance, 'ticket_status_changed',
                                f"Le statut de votre ticket \"{instance.title}\" est passé de '{old_status}' à '{instance.status}'")

            # Cas spécial pour résolu
            if instance.status.name == 'Résolu':
                create_notification(instance.created_by, instance, 'ticket_resolved',
                                    f"Votre ticket \"{instance.title}\" a été résolu. Veuillez confirmer si le problème est résolu.")
