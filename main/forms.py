from django import forms
from .models import Ticket

class TicketPurchaseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = []