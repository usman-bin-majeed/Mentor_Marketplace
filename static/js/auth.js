document.addEventListener('DOMContentLoaded', function() {
    // Form validation for signup
    const signupForm = document.querySelector('form[action*="signup"]');
    
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Simple validation
            if (username.length < 3) {
                event.preventDefault();
                alert('Username must be at least 3 characters long.');
                return;
            }
            
            if (!isValidEmail(email)) {
                event.preventDefault();
                alert('Please enter a valid email address.');
                return;
            }
            
            if (password.length < 6) {
                event.preventDefault();
                alert('Password must be at least 6 characters long.');
                return;
            }
        });
    }
    
    // Function to validate email format
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});