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

    window.handleNumberSelection(checkboxes[0]);

    const randomBonus = Math.floor(Math.random() * 14) + 1;
    radioButtons[randomBonus - 1].checked = true;
}

window.addTicket = function() {
    const ticketsContainer = document.getElementById('tickets-container');
    if (ticketsContainer.children.length < 10) {
        const newTicket = ticketsContainer.children[0].cloneNode(true);
        newTicket.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(input => {
            input.checked = false;
            input.disabled = false;
        });
        ticketsContainer.appendChild(newTicket);
    }
}

