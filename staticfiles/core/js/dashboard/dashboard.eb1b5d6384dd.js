document.addEventListener('DOMContentLoaded', function() {
    // Código JavaScript común para todas las páginas

    // Ejemplo: mostrar un mensaje de bienvenida
    console.log('Bienvenido a Cyberloto Bank');

    // Función para actualizar el contador
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

    // Dropdown menu functionality
    const dropdown = document.querySelector('.dropdown');
    const content = dropdown.querySelector('.dropdown-content');

    dropdown.addEventListener('mouseover', () => {
        content.style.display = 'block';
    });

    dropdown.addEventListener('mouseout', () => {
        content.style.display = 'none';
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const numbers = document.querySelectorAll(".number");
    numbers.forEach((number, index) => {
        setTimeout(() => {
            number.style.animationDelay = `${index * 0.2}s`;
            number.classList.add('animate');
        }, index * 200);
    });
});
