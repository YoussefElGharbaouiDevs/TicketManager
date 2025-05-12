from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from tickets.models import Ticket


@login_required
def agent_stats_dashboard(request):
    if request.user.role != 'agent':
        return redirect('home')  # ou erreur 403

    # Récupérer les tickets assignés à cet agent
    tickets = Ticket.objects.filter(assigned_to=request.user)

    # Grouper par statut
    stats = tickets.values('status__name').annotate(count=Count('id'))

    labels = [stat['status__name'] for stat in stats]
    data = [stat['count'] for stat in stats]

    return render(request, 'agent_stats_dashboard.html', {
        'labels': labels,
        'data': data
    })

