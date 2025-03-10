// Function to set current date minimum for datetime-local inputs
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    
    if (dateInputs.length > 0) {
        // Set minimum date to current date
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        const currentDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        
        dateInputs.forEach(input => {
            input.min = currentDateTime;
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const messages = document.querySelector('.messages');
    if (messages) {
        setTimeout(() => {
            messages.style.opacity = '0';
            setTimeout(() => {
                messages.style.display = 'none';
            }, 500);
        }, 5000);
    }
});