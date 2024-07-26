document.addEventListener('DOMContentLoaded', function() {
    // Código JavaScript específico para el dashboard

    function updateBalance() {
        fetch("{% url 'dashboard' %}", {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.querySelector('.text-right p').textContent = `Your current balance is: $${data.balance.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Actualizar balance al cargar la página
    updateBalance();
});
