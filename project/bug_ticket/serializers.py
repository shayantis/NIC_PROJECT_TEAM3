from rest_framework import serializers

from .models import (
    Ticket,
    TicketAssignment,
    TicketStatusHistory,
    TicketComment,
    Alert,
    TicketAttachment
)


class TicketSerializer(serializers.ModelSerializer):

    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'severity',
            'status',
            'created_by',
            'created_by_username',
            'office_id',
            'system_id',
            'created_at',
            'updated_at'
        ]


class TicketAssignmentSerializer(serializers.ModelSerializer):

    assigned_to_username = serializers.CharField(
        source='assigned_to.username',
        read_only=True
    )

    assigned_by_username = serializers.CharField(
        source='assigned_by.username',
        read_only=True
    )

    class Meta:
        model = TicketAssignment
        fields = [
            'id',
            'ticket',
            'assigned_to',
            'assigned_to_username',
            'assigned_by',
            'assigned_by_username',
            'assigned_at',
            'status'
        ]


class TicketStatusHistorySerializer(serializers.ModelSerializer):

    changed_by_username = serializers.CharField(
        source='changed_by.username',
        read_only=True
    )

    class Meta:
        model = TicketStatusHistory
        fields = [
            'id',
            'ticket',
            'old_status',
            'new_status',
            'changed_by',
            'changed_by_username',
            'changed_at'
        ]


class TicketCommentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = TicketComment
        fields = [
            'id',
            'ticket',
            'user',
            'username',
            'comment',
            'created_at'
        ]


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = [
            'id',
            'user',
            'ticket',
            'message',
            'is_read',
            'created_at'
        ]


class TicketAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketAttachment
        fields = [
            'id',
            'ticket',
            'file_name',
            'file_path',
            'uploaded_at'
        ]