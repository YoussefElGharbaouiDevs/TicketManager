from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from core.messages import AppMessages
from .forms import TicketForm, TicketStatusForm
from .models import Ticket, Status
from .services.agent_assignation_service import assign_agent


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'ticket_list.html', {'tickets': tickets})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.assigned_to = assign_agent(ticket.category)
            ticket.save()
            messages.success(request, AppMessages.ELEMENT_CREATED)
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'ticket_create.html', {'form': form})


@login_required
def ticket_detail_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user != ticket.assigned_to:
        return redirect('agent_dashboard')

    if request.method == 'POST':
        form = TicketStatusForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, AppMessages.ELEMENT_UPDATED)
            return redirect('agent_dashboard')
    else:
        form = TicketStatusForm(instance=ticket)

    return render(request, 'ticket_detail_edit.html', {'ticket': ticket, 'form': form})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    return render(request, 'ticket_detail.html', {'ticket': ticket})


@login_required
def agent_dashboard(request):
    if request.user.role != 'agent':
        return redirect('home')  # or show permission denied
    tickets = Ticket.objects.filter(assigned_to=request.user)
    return render(request, 'agent_dashboard.html', {'tickets': tickets})

@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status.name == "Résolu":
        closed_status = Status.objects.get(pk=4) # Status -> Fermé
        ticket.status = closed_status
        ticket.save()
        messages.success(request, AppMessages.TICKET_CLOSED)
    else:
        messages.warning(request, AppMessages.ERROR_GENERIC)

    return redirect('ticket_list')