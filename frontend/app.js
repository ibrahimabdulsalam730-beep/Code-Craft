
// The public URL of your deployed Python backend
const API_URL = 'https://your-backend-url.com'; // <-- IMPORTANT: Replace with your actual backend URL

// Demo button functionality
document.addEventListener('DOMContentLoaded', function() {
    const demoBtn = document.getElementById('demo-btn');
    
    if (demoBtn) {
        demoBtn.addEventListener('click', function() {
            alert('Welcome to your frontend app! This is deployed on Netlify.');
            console.log('Demo button clicked!');
        });
    }
});

// Login form functionality (if you add a login form later)
function handleLogin() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = event.target.email.value;
            const password = event.target.password.value;

            try {
                const response = await fetch(`${API_URL}/api/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    console.log('Login successful!', data);
                    // Store the token, redirect the user, etc.
                } else {
                    console.error('Login failed:', data.message);
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        });
    }
}

// Initialize login functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', handleLogin);

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
