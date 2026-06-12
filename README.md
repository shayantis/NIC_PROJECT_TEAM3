# NIC Bug Tracker

A web-based Bug / Ticket Tracking System developed using Django and Django REST Framework for managing software and technical issue reports inside an organization.

## Features

- Dashboard with ticket statistics
- Create and manage tickets
- Update ticket status
- Assign tickets to users
- Add comments to tickets
- Upload ticket attachments
- Automatic alerts on ticket assignment
- Email notification using SMTP on ticket creation
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
- PostgreSQL
- SMTP Email Service

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

## SMTP Configuration

Create a `.env` file and add:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
```

## Ticket Status

- OPEN
- ASSIGNED
- IN_PROGRESS
- CLOSED
