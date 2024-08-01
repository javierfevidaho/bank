document.addEventListener('DOMContentLoaded', function() {
    // Código JavaScript específico para la página del carrito

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

    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const url = this.getAttribute('href');
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('tr').remove();
                    updateCartCount();
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    updateCartCount();
});
