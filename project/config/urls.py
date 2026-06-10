from django.contrib import admin
from django.urls import path, include

from bug_ticket.views import dashboard_page

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        dashboard_page,
        name='home'
    ),

    path(
        'api/tickets/',
        include('bug_ticket.urls')
    ),

]