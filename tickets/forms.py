from django import forms
from .models import Ticket, Status


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'priority', 'attached_files']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    def save(self, commit=True):
        ticket = super().save(commit=False)
        ticket.status = Status.objects.get(pk=1)  # Automatically set to 'Nouveau'
        if commit:
            ticket.save()
        return ticket



class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.exclude(pk=4)
