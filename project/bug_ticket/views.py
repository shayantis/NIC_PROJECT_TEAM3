from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, redirect

from users.models import User

from .models import (
    Ticket,
    TicketAssignment,
    TicketStatusHistory,
    TicketComment,
    Alert
)

from .serializers import (
    TicketSerializer,
    TicketAssignmentSerializer,
    TicketCommentSerializer
)


# =========================
# API VIEWS
# =========================

class CreateTicketView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Ticket Created Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TicketListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tickets = Ticket.objects.all().order_by('-created_at')

        serializer = TicketSerializer(
            tickets,
            many=True
        )

        return Response(serializer.data)


class AssignTicketView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TicketAssignmentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            assignment = serializer.save()

            assignment.ticket.status = 'ASSIGNED'
            assignment.ticket.save()

            Alert.objects.create(
                user=assignment.assigned_to,
                ticket=assignment.ticket,
                message="New ticket assigned to you"
            )

            return Response(
                {
                    "message": "Ticket Assigned Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UpdateTicketStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        ticket_id = request.data.get("ticket_id")
        new_status = request.data.get("status")
        changed_by = request.data.get("changed_by")

        if not ticket_id or not new_status or not changed_by:

            return Response(
                {
                    "error": "ticket_id, status and changed_by are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            ticket = Ticket.objects.get(
                id=ticket_id
            )

        except Ticket.DoesNotExist:

            return Response(
                {
                    "error": "Ticket not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = ticket.status

        ticket.status = new_status
        ticket.save()

        TicketStatusHistory.objects.create(
            ticket=ticket,
            old_status=old_status,
            new_status=new_status,
            changed_by_id=changed_by
        )

        Alert.objects.create(
            user=ticket.created_by,
            ticket=ticket,
            message=f"Ticket status updated to {new_status}"
        )

        return Response(
            {
                "message": "Status Updated Successfully"
            }
        )


class AddCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TicketCommentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            comment = serializer.save()

            Alert.objects.create(
                user=comment.ticket.created_by,
                ticket=comment.ticket,
                message="New comment added to ticket"
            )

            return Response(
                {
                    "message": "Comment Added Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_tickets = Ticket.objects.count()

        open_tickets = Ticket.objects.filter(
            status='OPEN'
        ).count()

        assigned_tickets = Ticket.objects.filter(
            status='ASSIGNED'
        ).count()

        closed_tickets = Ticket.objects.filter(
            status='CLOSED'
        ).count()

        critical_tickets = Ticket.objects.filter(
            severity='CRITICAL'
        ).count()

        return Response({
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "assigned_tickets": assigned_tickets,
            "closed_tickets": closed_tickets,
            "critical_tickets": critical_tickets
        })


# =========================
# FRONTEND PAGES
# =========================

def dashboard_page(request):

    total_tickets = Ticket.objects.count()

    open_tickets = Ticket.objects.filter(
        status='OPEN'
    ).count()

    assigned_tickets = Ticket.objects.filter(
        status='ASSIGNED'
    ).count()

    closed_tickets = Ticket.objects.filter(
        status='CLOSED'
    ).count()

    context = {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "assigned_tickets": assigned_tickets,
        "closed_tickets": closed_tickets
    }

    return render(
        request,
        'bug_ticket/dashboard.html',
        context
    )


def tickets_page(request):

    tickets = Ticket.objects.all().order_by('-created_at')

    context = {
        "tickets": tickets
    }

    return render(
        request,
        'bug_ticket/tickets.html',
        context
    )


def login_page(request):

    return render(
        request,
        'bug_ticket/login.html'
    )


def create_ticket_page(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        severity = request.POST.get("severity")

        admin_user = User.objects.first()

        ticket = Ticket.objects.create(
            title=title,
            description=description,
            severity=severity,
            status='OPEN',
            created_by=admin_user
        )

        if severity == 'CRITICAL':

            Alert.objects.create(
                user=admin_user,
                ticket=ticket,
                message="Critical ticket created"
            )

        return redirect('/api/tickets/tickets-page/')

    return render(
        request,
        'bug_ticket/create_ticket.html'
    )


def ticket_detail_page(request, ticket_id):

    ticket = Ticket.objects.get(id=ticket_id)

    comments = TicketComment.objects.filter(
        ticket=ticket
    ).order_by('-created_at')

    if request.method == "POST":

        comment_text = request.POST.get("comment")

        admin_user = User.objects.first()

        TicketComment.objects.create(
            ticket=ticket,
            user=admin_user,
            comment=comment_text
        )

        Alert.objects.create(
            user=ticket.created_by,
            ticket=ticket,
            message="New comment added to ticket"
        )

        return redirect(
            f'/api/tickets/ticket/{ticket.id}/'
        )

    context = {
        "ticket": ticket,
        "comments": comments
    }

    return render(
        request,
        'bug_ticket/ticket_detail.html',
        context
    )


def update_status_page(request, ticket_id):

    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":

        new_status = request.POST.get("status")

        old_status = ticket.status

        ticket.status = new_status
        ticket.save()

        admin_user = User.objects.first()

        TicketStatusHistory.objects.create(
            ticket=ticket,
            old_status=old_status,
            new_status=new_status,
            changed_by=admin_user
        )

        Alert.objects.create(
            user=ticket.created_by,
            ticket=ticket,
            message=f"Ticket status updated to {new_status}"
        )

    return redirect(
        f'/api/tickets/ticket/{ticket.id}/'
    )


def assign_ticket_page(request, ticket_id):

    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":

        assigned_to_id = request.POST.get("assigned_to")

        assigned_user = User.objects.get(
            id=assigned_to_id
        )

        admin_user = User.objects.first()

        TicketAssignment.objects.create(
            ticket=ticket,
            assigned_to=assigned_user,
            assigned_by=admin_user,
            status='ASSIGNED'
        )

        ticket.status = 'ASSIGNED'
        ticket.save()

        Alert.objects.create(
            user=assigned_user,
            ticket=ticket,
            message="New ticket assigned to you"
        )

    return redirect(
        f'/api/tickets/ticket/{ticket.id}/'
    )