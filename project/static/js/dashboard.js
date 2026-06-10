fetch('/dashboard/')
.then(response => response.json())
.then(data => {

    document.getElementById('totalTickets').innerText =
        data.total_tickets;

    document.getElementById('openTickets').innerText =
        data.open_tickets;

    document.getElementById('assignedTickets').innerText =
        data.assigned_tickets;

    document.getElementById('closedTickets').innerText =
        data.closed_tickets;
});