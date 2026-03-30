// Form Validation
(function() {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();

// Email Validation
document.querySelector('input[type="email"]')?.addEventListener('blur', function() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.value)) {
        this.classList.add('validation-error');
    } else {
        this.classList.remove('validation-error');
    }
});

// Year Validation
document.querySelectorAll('input[type="number"]').forEach(input => {
    if (input.name.includes('year')) {
        input.addEventListener('blur', function() {
            const currentYear = new Date().getFullYear();
            const year = parseInt(this.value);
            
            if (year && (year < 1990 || year > currentYear + 1)) {
                this.classList.add('validation-error');
            } else {
                this.classList.remove('validation-error');
            }
        });
    }
});

// Auto-save functionality
let autoSaveTimer;
document.querySelectorAll('input, textarea, select').forEach(field => {
    field.addEventListener('input', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(() => {
            localStorage.setItem('ba_resume_form', JSON.stringify(getFormData()));
        }, 1000);
    });
});

function getFormData() {
    const formData = {};
    document.querySelectorAll('input, textarea, select').forEach(field => {
        formData[field.name] = field.value;
    });
    return formData;
}

// Load saved data on page load
window.addEventListener('load', function() {
    const savedData = localStorage.getItem('ba_resume_form');
    if (savedData) {
        const data = JSON.parse(savedData);
        for (const [name, value] of Object.entries(data)) {
            const field = document.querySelector(`[name="${name}"]`);
            if (field) {
                field.value = value;
            }
        }
    }
});

// Clear saved data on form submit
document.querySelector('form')?.addEventListener('submit', function() {
    localStorage.removeItem('ba_resume_form');
});
