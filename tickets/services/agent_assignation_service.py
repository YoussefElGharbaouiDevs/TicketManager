from django.db.models import Count

from accounts.models import CustomUser


def assign_agent(category):
    agents = CustomUser.objects.filter(role='agent', categories=category)

    # Among agents in this category, get the one with the fewest assigned tickets
    agent = agents.annotate(ticket_count=Count('assigned_tickets')).order_by('ticket_count').first()

    return agent
