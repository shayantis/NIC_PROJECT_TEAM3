from django.urls import path

from .views import (
    CreateTicketView,
    TicketListView,
    AssignTicketView,
    UpdateTicketStatusView,
    AddCommentView,
    DashboardView
)

urlpatterns = [

    path(
        'create/',
        CreateTicketView.as_view()
    ),

    path(
        'list/',
        TicketListView.as_view()
    ),

    path(
        'assign/',
        AssignTicketView.as_view()
    ),

    path(
        'status/',
        UpdateTicketStatusView.as_view()
    ),

    path(
        'comment/',
        AddCommentView.as_view()
    ),
    
    path(
    'dashboard/',
    DashboardView.as_view()
),

]