// Theme Toggle Functionality
function toggleTheme() {
    const body = document.body;
    const themeToggle = document.querySelector('.theme-toggle');
    
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeToggle.textContent = '☀️';
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeToggle.textContent = '🌙';
        localStorage.setItem('theme', 'dark');
    }
}

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[$@#&!]+/)) strength++;
    
    return strength;
}

// Initialize password strength indicators
document.addEventListener('DOMContentLoaded', function() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        const strengthBar = document.createElement('div');
        strengthBar.className = 'password-strength';
        input.parentNode.appendChild(strengthBar);
        
        input.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            strengthBar.className = 'password-strength';
            
            if (this.value.length > 0) {
                if (strength < 2) {
                    strengthBar.classList.add('strength-weak');
                } else if (strength < 4) {
                    strengthBar.classList.add('strength-fair');
                } else if (strength < 5) {
                    strengthBar.classList.add('strength-good');
                } else {
                    strengthBar.classList.add('strength-strong');
                }
            }
        });
    });
});

// Initialize theme from localStorage
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const themeToggle = document.querySelector('.theme-toggle');
    
    if (savedTheme === 'light') {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
        if (themeToggle) themeToggle.textContent = '☀️';
    } else {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
        if (themeToggle) themeToggle.textContent = '🌙';
    }

    // Add floating animation to cards
    animateFloatingCards();
    
    // Add scroll effects to navbar
    window.addEventListener('scroll', handleScroll);
});

// Floating cards animation
function animateFloatingCards() {
    const cards = document.querySelectorAll('.floating-1, .floating-2, .floating-3');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 2}s`;
    });
}

// Navbar scroll effect
function handleScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(15, 15, 26, 0.95)';
        navbar.style.backdropFilter = 'blur(20px)';
    } else {
        navbar.style.background = '';
        navbar.style.backdropFilter = '';
    }
}

// Form validation and enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add focus effects to form inputs
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });

    // Add character counter to textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.style.textAlign = 'right';
        counter.style.fontSize = '0.8rem';
        counter.style.color = 'var(--text-secondary)';
        counter.style.marginTop = '0.5rem';
        textarea.parentNode.appendChild(counter);

        function updateCounter() {
            const maxLength = textarea.getAttribute('maxlength') || 500;
            counter.textContent = `${textarea.value.length}/${maxLength}`;
            
            if (textarea.value.length > maxLength * 0.8) {
                counter.style.color = '#ff6b6b';
            } else {
                counter.style.color = 'var(--text-secondary)';
            }
        }

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading states to buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button[type="submit"], .btn-primary');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.type === 'submit' || this.classList.contains('btn-primary')) {
                const form = this.closest('form');
                if (form && form.checkValidity()) {
                    this.innerHTML = '<span class="loading-spinner"></span> Loading...';
                    this.disabled = true;
                    setTimeout(() => {
                        this.innerHTML = this.getAttribute('data-original-text') || this.textContent;
                        this.disabled = false;
                    }, 3000);
                }
            }
        });
    });
});

// Custom confirmation dialogs
function confirmAction(message = 'Are you sure?') {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'confirm-modal glass';
        modal.innerHTML = `
            <div class="modal-content">
                <p>${message}</p>
                <div class="modal-buttons">
                    <button class="btn-secondary cancel-btn">Cancel</button>
                    <button class="btn-primary confirm-btn">Confirm</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.querySelector('.cancel-btn').addEventListener('click', () => {
            document.body.removeChild(modal);
            resolve(false);
        });
        
        modal.querySelector('.confirm-btn').addEventListener('click', () => {
            document.body.removeChild(modal);
            resolve(true);
        });
    });
}

// Enhanced error handling for API calls
async function handleApiCall(apiCall) {
    try {
        const response = await apiCall();
        return response;
    } catch (error) {
        console.error('API Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
        throw error;
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} glass`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem 2rem;
        border-radius: 10px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid transparent;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 8px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .confirm-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    }
    
    .modal-content {
        padding: 2rem;
        text-align: center;
        max-width: 400px;
        width: 90%;
    }
    
    .modal-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 1.5rem;
    }
    
    .notification-error {
        border-left: 4px solid #ff6b6b;
    }
    
    .notification-success {
        border-left: 4px solid #51cf66;
    }
    
    .notification-info {
        border-left: 4px solid var(--neon-cyan);
    }
`;
document.head.appendChild(style);
