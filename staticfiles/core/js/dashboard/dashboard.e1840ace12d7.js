document.addEventListener('DOMContentLoaded', function() {
    // Función para actualizar el contador con el diseño de "flip clock"
    function updateFlipClock() {
        const eventDate = new Date('September 7, 2024 00:00:00').getTime();
        const now = new Date().getTime();
        const distance = eventDate - now;

        if (distance < 0) {
            document.querySelector('.flip-clock').innerHTML = "Draw has ended!";
            return;
        }

        const days = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, '0');
        const hours = String(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
        const minutes = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
        const seconds = String(Math.floor((distance % (1000 * 60)) / 1000)).padStart(2, '0');

        flipDigits('days1', days[0]);
        flipDigits('days2', days[1]);
        flipDigits('hours1', hours[0]);
        flipDigits('hours2', hours[1]);
        flipDigits('minutes1', minutes[0]);
        flipDigits('minutes2', minutes[1]);
        flipDigits('seconds1', seconds[0]);
        flipDigits('seconds2', seconds[1]);
    }

    function flipDigits(id, newValue) {
        const card = document.getElementById(id);
        const front = card.querySelector('.flip-card-front');
        const back = card.querySelector('.flip-card-back');

        if (front.textContent !== newValue) {
            back.textContent = newValue;
            card.classList.add('flip');
            
            setTimeout(() => {
                front.textContent = newValue;
                card.classList.remove('flip');
            }, 600);
        }
    }

    setInterval(updateFlipClock, 1000);
    updateFlipClock();
});
