from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from core.messages import AppMessages
from .forms import TicketForm, TicketStatusForm, CommentForm
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

    # Récupérer les commentaires liés à ce ticket
    comments = ticket.comments.all().order_by('-created_at')

    # Gestion des formulaires
    status_form = TicketStatusForm(request.POST or None, instance=ticket)
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if 'status_submit' in request.POST and status_form.is_valid():
            status_form.save()
            messages.success(request, AppMessages.ELEMENT_UPDATED)
            return redirect('ticket_detail_edit', pk=pk)

        elif 'comment_submit' in request.POST and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect('ticket_detail_edit', pk=pk)

    return render(request, 'ticket_detail_edit.html', {
        'ticket': ticket,
        'status_form': status_form,
        'comment_form': comment_form,
        'comments': comments,
    })

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    comments = ticket.comments.select_related('author').order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect('ticket_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'form': form
    })

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