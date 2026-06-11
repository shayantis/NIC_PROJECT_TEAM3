from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home_redirect(request):
    return redirect('/api/tickets/dashboard-page/')


urlpatterns = [
    path('', home_redirect),

    path('admin/', admin.site.urls),

    path(
        'api/tickets/',
        include('bug_ticket.urls')
    ),

    path(
        'api/users/',
        include('users.urls')
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)