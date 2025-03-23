document.addEventListener('DOMContentLoaded', () => {
    const formBox = document.querySelector('.form-box');
    const showSignupLink = document.getElementById('show-signup');
    const showLoginLink = document.getElementById('show-login');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    showSignupLink.addEventListener('click', (e) => {
        e.preventDefault();
        formBox.classList.add('flipped');
    });

    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        formBox.classList.remove('flipped');
    });


    // Add subtle animation to form inputs
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.style.transform = 'translateY(-5px)';
        });
        input.addEventListener('blur', () => {
            input.parentElement.style.transform = 'translateY(0)';
        });
    });

    // Initialize Lucide icons
    lucide.createIcons();
});

