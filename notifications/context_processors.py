def notifications_processor(request):

    context = {
        'recent_notifications': [],
        'unread_count': 0
    }

    if request.user.is_authenticated:
        # Obtenir les 5 notifications les plus récentes
        context['recent_notifications'] = request.user.notifications.all()[:5]

        # Compter les notifications non lues
        context['unread_count'] = request.user.notifications.filter(is_read=False).count()

    return context