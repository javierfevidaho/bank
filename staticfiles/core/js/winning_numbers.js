// winning_numbers.js

// If there are any JavaScript functionalities needed for the Winning Numbers page, add them here

// Example: Adding an alert for when a new draw date is added
document.addEventListener('DOMContentLoaded', (event) => {
    const drawDateCells = document.querySelectorAll('td:nth-child(1)');
    drawDateCells.forEach(cell => {
        cell.addEventListener('click', () => {
            alert(`You clicked on draw date: ${cell.textContent}`);
        });
    });
});
