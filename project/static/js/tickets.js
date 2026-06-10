fetch('/list/')
.then(response => response.json())
.then(data => {

    let table = document.getElementById('ticketTable');

    data.forEach(ticket => {

        table.innerHTML += `
            <tr>
                <td>${ticket.title}</td>
                <td>${ticket.severity}</td>
                <td>${ticket.status}</td>
            </tr>
        `;
    });
});