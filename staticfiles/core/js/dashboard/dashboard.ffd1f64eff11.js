document.addEventListener('DOMContentLoaded', function() {
    function updateFlipClock() {
        const eventDate = new Date('September 7, 2024 00:00:00').getTime();
        const now = new Date().getTime();
        const distance = eventDate - now;

        if (distance < 0) {
            document.getElementById('flip-clock').innerHTML = "Draw has ended!";
            return;
        }

        const days = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, '0');
        const hours = String(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
        const minutes = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
        const seconds = String(Math.floor((distance % (1000 * 60)) / 1000)).padStart(2, '0');

        updateFlipCard('days1', days);
        updateFlipCard('hours1', hours);
        updateFlipCard('minutes1', minutes);
        updateFlipCard('seconds1', seconds);
    }

    function updateFlipCard(id, value) {
        const topCard = document.getElementById(id);
        const bottomCard = topCard.nextElementSibling;

        if (topCard.textContent !== value) {
            topCard.textContent = value;
            topCard.style.transform = 'rotateX(-180deg)';
            bottomCard.style.transform = 'rotateX(0deg)';

            setTimeout(() => {
                bottomCard.textContent = value;
                topCard.style.transform = 'rotateX(0deg)';
                bottomCard.style.transform = 'rotateX(180deg)';
            }, 300);
        }
    }

    setInterval(updateFlipClock, 1000);
    updateFlipClock();
});
