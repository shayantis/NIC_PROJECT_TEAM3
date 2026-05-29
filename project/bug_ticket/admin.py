from django.contrib import admin
from .models import (
    Ticket,
    TicketAssignment,
    TicketStatusHistory,
    TicketComment,
    Alert,
    TicketAttachment
)

admin.site.register(Ticket)
admin.site.register(TicketAssignment)
admin.site.register(TicketStatusHistory)
admin.site.register(TicketComment)
admin.site.register(Alert)
admin.site.register(TicketAttachment)