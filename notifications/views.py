from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    """
    Affiche la liste des notifications de l'utilisateur courant.
    """
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notification_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    """
    Marque une notification comme lue.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')

@login_required
def mark_all_as_read(request):
    """
    Marque toutes les notifications comme lues.
    """
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notification_list')
