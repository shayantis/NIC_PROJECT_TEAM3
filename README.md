# NIC Bug Tracker

A web-based Bug / Ticket Tracking System developed using Django and Django REST Framework for managing software and technical issue reports inside an organization.

## Features

- Dashboard with ticket statistics
- Create and manage tickets
- Update ticket status
- Assign tickets to users
- Add comments to tickets
- Automatic alerts on ticket assignment
- Django Admin Panel support

## Main Entities / Models

- Ticket
- TicketAssignment
- TicketComment
- TicketStatusHistory
- TicketAttachment
- Alert

## Tech Stack

- Python
- Django
- Django REST Framework
- HTML
- CSS
- JavaScript
- SQLite

## Run Project

```bash
python manage.py runserver
```

## Main URLs

Frontend:

```bash
http://127.0.0.1:8000/
```

Admin Panel:

```bash
http://127.0.0.1:8000/admin/
```

## Ticket Status

- OPEN
- ASSIGNED
- IN_PROGRESS
- CLOSED
