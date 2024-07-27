document.addEventListener('DOMContentLoaded', function() {
    // Common JavaScript for all pages
    console.log('Bienvenido a Cyberloto Bank');

    // Function to update the countdown
    function updateCountdown() {
        const eventDate = new Date('September 7, 2024 00:00:00').getTime();
        const now = new Date().getTime();
        const distance = eventDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById('days').textContent = days;
        document.getElementById('hours').textContent = hours;
        document.getElementById('minutes').textContent = minutes;
        document.getElementById('seconds').textContent = seconds;

        if (distance < 0) {
            document.querySelector('.countdown-container').innerHTML = "Draw has ended!";
        }
    }

    setInterval(updateCountdown, 1000);
    updateCountdown();
});

document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.querySelector('.dropdown');
    dropdown.addEventListener('mouseover', () => {
        const content = dropdown.querySelector('.dropdown-content');
        content.style.display = 'block';
    });

    dropdown.addEventListener('mouseout', () => {
        const content = dropdown.querySelector('.dropdown-content');
        content.style.display = 'none';
    });
});
