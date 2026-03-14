document.addEventListener('DOMContentLoaded', () => {
    // --- MODAL LOGIC ---
    const authModal = document.getElementById('authModal');
    const loginBtn = document.getElementById('loginBtn');
    const heroLoginBtn = document.getElementById('heroLoginBtn');
    const closeAuthBtn = document.getElementById('closeAuth');
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const toRegisterBtn = document.getElementById('toRegister');
    const toLoginBtn = document.getElementById('toLogin');

    function openModal() {
        if(authModal) {
            authModal.classList.add('active');
            loginView.style.display = 'block';
            registerView.style.display = 'none';
        }
    }

    if(loginBtn) loginBtn.addEventListener('click', openModal);
    if(heroLoginBtn) heroLoginBtn.addEventListener('click', openModal);

    if(closeAuthBtn) {
        closeAuthBtn.addEventListener('click', () => {
            authModal.classList.remove('active');
        });
    }

    if(authModal) {
        authModal.addEventListener('click', (e) => {
            if (e.target === authModal) {
                authModal.classList.remove('active');
            }
        });
    }

    if(toRegisterBtn) {
        toRegisterBtn.addEventListener('click', () => {
            loginView.style.display = 'none';
            registerView.style.display = 'block';
        });
    }

    if(toLoginBtn) {
        toLoginBtn.addEventListener('click', () => {
            registerView.style.display = 'none';
            loginView.style.display = 'block';
        });
    }

    // --- FLASH TOAST LOGIC ---
    setTimeout(() => {
        const flashContainer = document.querySelector('.flash-container');
        if(flashContainer) {
            flashContainer.style.opacity = '0';
            flashContainer.style.transition = 'opacity 0.5s ease';
            setTimeout(() => flashContainer.remove(), 500);
        }
    }, 4000);

    // --- THEME TOGGLE LOGIC ---
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    if (themeToggle) {
        const themeIcon = themeToggle.querySelector('i');
        
        const currentTheme = localStorage.getItem('crms_theme');
        if (currentTheme === 'light') {
            body.classList.add('light-theme');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }

        themeToggle.addEventListener('click', () => {
            body.classList.toggle('light-theme');
            
            if (body.classList.contains('light-theme')) {
                localStorage.setItem('crms_theme', 'light');
                themeIcon.classList.replace('fa-moon', 'fa-sun');
            } else {
                localStorage.setItem('crms_theme', 'dark');
                themeIcon.classList.replace('fa-sun', 'fa-moon');
            }
        });
    }

    // --- ADD RESOURCE FORM LOGIC ---
    const resourceTypeSelect = document.querySelector('select[name="resource_type"]');
    const departmentSelect = document.querySelector('select[name="department_id"]');

    if (resourceTypeSelect && departmentSelect) {
        resourceTypeSelect.addEventListener('change', function() {
            if (this.value === 'Centralised Facility') {
                // Blur and disable the department field
                departmentSelect.style.opacity = '0.4';
                departmentSelect.style.cursor = 'not-allowed';
                departmentSelect.disabled = true; 
                departmentSelect.required = false; // Remove required so the form can submit
                departmentSelect.value = ""; // Clear any previously selected value
            } else {
                // Restore the department field for other types (Lab, Venue, etc.)
                departmentSelect.style.opacity = '1';
                departmentSelect.style.cursor = 'pointer';
                departmentSelect.disabled = false;
                departmentSelect.required = true;
            }
        });
    }
});
