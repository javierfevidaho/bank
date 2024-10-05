document.addEventListener('DOMContentLoaded', function() {
    // Mostrar mensaje de bienvenida
    console.log('Bienvenido a Cyber Lotto Bank');

    // Función para actualizar el contador de cuenta regresiva
    function updateCountdown() {
        // Cambia esta fecha a la próxima fecha de sorteo
        const eventDate = new Date('2024-10-07T00:00:00').getTime();
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
            clearInterval(countdownInterval);
        }
    }

    // Ejecutar la función de cuenta regresiva cada segundo
    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown();

    // Funcionalidad del menú desplegable (si es necesario)
    const dropdown = document.querySelector('.dropdown');
    if (dropdown) {
        const content = dropdown.querySelector('.dropdown-content');

        dropdown.addEventListener('mouseover', () => {
            content.style.display = 'block';
        });

        dropdown.addEventListener('mouseout', () => {
            content.style.display = 'none';
        });
    }

    // Animación escalonada de números ganadores
    const numbers = document.querySelectorAll(".number");
    numbers.forEach((number, index) => {
        setTimeout(() => {
            number.style.animationDelay = `${index * 0.2}s`;
            number.classList.add('animate');
        }, index * 200);
    });
});
