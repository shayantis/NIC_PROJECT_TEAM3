from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class CreateTicketView(APIView):

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

    def get(self, request):

        tickets = Ticket.objects.all()

        serializer = TicketSerializer(
            tickets,
            many=True
        )

        return Response(serializer.data)


class AssignTicketView(APIView):

    def post(self, request):

        serializer = TicketAssignmentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            assignment = serializer.save()

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

    def post(self, request):

        ticket_id = request.data.get("ticket_id")
        new_status = request.data.get("status")
        changed_by = request.data.get("changed_by")

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

        return Response(
            {
                "message": "Status Updated Successfully"
            }
        )


class AddCommentView(APIView):

    def post(self, request):

        serializer = TicketCommentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

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

        return Response({
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "assigned_tickets": assigned_tickets,
            "closed_tickets": closed_tickets
        })