
// The public URL of your deployed Python backend
const API_URL = 'https://your-backend-url.com'; // <-- IMPORTANT: Replace with your actual backend URL

document.getElementById('login-form').addEventListener('submit', async (event) => {
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
