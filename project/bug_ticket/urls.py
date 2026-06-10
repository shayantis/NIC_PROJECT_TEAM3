from django.urls import path

from .views import (
    dashboard_page,
    tickets_page,
    login_page,
    create_ticket_page,
    ticket_detail_page,
    update_status_page,
    assign_ticket_page
)

urlpatterns = [

    path(
        'dashboard-page/',
        dashboard_page,
        name='dashboard-page'
    ),

    path(
        'tickets-page/',
        tickets_page,
        name='tickets-page'
    ),

    path(
        'login-page/',
        login_page,
        name='login-page'
    ),

    path(
        'create-ticket/',
        create_ticket_page,
        name='create-ticket'
    ),

    path(
        'ticket/<int:ticket_id>/',
        ticket_detail_page,
        name='ticket-detail'
    ),

    path(
        'update-status/<int:ticket_id>/',
        update_status_page,
        name='update-status'
    ),

    path(
        'assign-ticket/<int:ticket_id>/',
        assign_ticket_page,
        name='assign-ticket'
    ),

]