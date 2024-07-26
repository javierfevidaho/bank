window.handleNumberSelection = function(checkbox) {
    const form = checkbox.closest('form');
    const checkboxes = form.querySelectorAll('input[type="checkbox"][name="numbers"]');
    const selectedCount = Array.from(checkboxes).filter(cb => cb.checked).length;

    checkboxes.forEach(cb => {
        if (selectedCount >= 5 && !cb.checked) {
            cb.disabled = true;
        } else {
            cb.disabled = false;
        }
    });
}

window.autoSelectNumbers = function(button) {
    const form = button.closest('form');
    const checkboxes = form.querySelectorAll('input[type="checkbox"][name="numbers"]');
    checkboxes.forEach(cb => cb.checked = false);
    const radioButtons = form.querySelectorAll('input[type="radio"][name="bonus"]');
    radioButtons.forEach(rb => rb.checked = false);

    let selectedNumbers = [];
    while (selectedNumbers.length < 5) {
        const randomNum = Math.floor(Math.random() * 35) + 1;
        if (!selectedNumbers.includes(randomNum)) {
            selectedNumbers.push(randomNum);
        }
    }

    selectedNumbers.forEach(num => {
        checkboxes[num - 1].checked = true;
    });

    handleNumberSelection(checkboxes[0]);

    const randomBonus = Math.floor(Math.random() * 13) + 1;
    radioButtons[randomBonus - 1].checked = true;
}

window.addToCart = function() {
    const form = document.getElementById('ticket-form');
    const formData = new FormData(form);
    fetch("{% url 'purchase_ticket' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.success);
            updateCartCount();
            form.reset();
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateCartCount() {
    fetch("{% url 'view_cart' %}", {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-count').textContent = data.cart_items_count;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

window.addBulkToCart = function() {
    const quantity = document.getElementById('quantity').value;
    const tickets = generateTickets(quantity);
    const bulkNumbersDiv = document.getElementById('bulkNumbers');
    bulkNumbersDiv.innerHTML = '';
    tickets.forEach((ticket, index) => {
        const ticketDiv = document.createElement('div');
        ticketDiv.textContent = `Ticket ${index + 1}: Numbers: ${ticket.numbers.join(', ')}, Bonus: ${ticket.bonus}`;
        bulkNumbersDiv.appendChild(ticketDiv);
    });
    document.getElementById('bulkNumbersFrame').style.display = 'block';
}

function generateTickets(quantity) {
    const tickets = [];
    for (let i = 0; i < quantity; i++) {
        const numbers = [];
        while (numbers.length < 5) {
            const randomNum = Math.floor(Math.random() * 35) + 1;
            if (!numbers.includes(randomNum)) {
                numbers.push(randomNum);
            }
        }
        const bonus = Math.floor(Math.random() * 14) + 1;
        tickets.push({ numbers, bonus });
    }
    return tickets;
}

function closeModal() {
    document.getElementById('bulkModal').style.display = 'none';
}

window.confirmBulk = function() {
    const tickets = [];
    const bulkNumbersDiv = document.getElementById('bulkNumbers').children;
    for (let i = 0; i < bulkNumbersDiv.length; i++) {
        const ticketText = bulkNumbersDiv[i].textContent;
        const numbers = ticketText.match(/Numbers: (.*), Bonus/)[1].split(', ').map(Number);
        const bonus = parseInt(ticketText.match(/Bonus: (\d+)/)[1]);
        tickets.push({ numbers, bonus });
    }

    const formData = new FormData();
    formData.append('bulk_tickets', JSON.stringify(tickets));
    fetch("{% url 'purchase_ticket' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.success);
            updateCartCount();
            document.getElementById('bulkNumbersFrame').style.display = 'none';
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', updateCartCount);
