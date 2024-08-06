document.addEventListener('DOMContentLoaded', function() {
    // Código JavaScript específico para el perfil

    function updateProfile(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        
        fetch("{% url 'profile' %}", {
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
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    document.querySelector('.profile-container form').addEventListener('submit', updateProfile);
});
