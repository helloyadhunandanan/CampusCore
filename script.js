// --- 1. Navbar Scroll Effect ---
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// --- 2. 3D Tilt Effect for Feature Cards ---
const cards = document.querySelectorAll('.feature-card');
cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -10;
        const rotateY = ((x - centerX) / centerX) * 10;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
    });
});

// --- 3. Modal Universal Controls ---
const authModal = document.getElementById('authModal');
const bookingModal = document.getElementById('bookingModal');
const catalogModal = document.getElementById('catalogModal');

function toggleModal(id, state) {
    const element = document.getElementById(id);
    if (!element) return;
    if (state === 'open') element.classList.add('active');
    else element.classList.remove('active');
}

// Event Listeners for Opening Modals
document.getElementById('navLoginBtn')?.addEventListener('click', () => toggleModal('authModal', 'open'));
document.getElementById('mainBookBtn')?.addEventListener('click', () => toggleModal('bookingModal', 'open'));
document.getElementById('mainCatalogBtn')?.addEventListener('click', () => toggleModal('catalogModal', 'open'));

// Global Close Listeners for All Modals
document.querySelectorAll('.close-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.target.closest('.modal-overlay').classList.remove('active');
    });
});

// Close when clicking on the blurred background
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

// --- 4. Auth View Switching (Login <-> Register) ---
document.getElementById('toRegister')?.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('loginView').style.display = 'none';
    document.getElementById('registerView').style.display = 'block';
});

document.getElementById('toLogin')?.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('registerView').style.display = 'none';
    document.getElementById('loginView').style.display = 'block';
});

// --- 5. Registration Integration ---
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: e.target.querySelector('input[type="text"]').value,
            email: e.target.querySelector('input[type="email"]').value,
            password: e.target.querySelector('input[type="password"]').value
        };

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const resData = await response.json();

            if (response.ok) {
                showToast("Account Created! Sign in now. 🚀");
                document.getElementById('toLogin').click();
            } else {
                showToast("Error: " + resData.message);
            }
        } catch (error) {
            showToast("Connection failed.");
        }
    });
}

// --- 6. Login Integration & Redirect ---
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            email: e.target.querySelector('input[type="text"]').value,
            password: e.target.querySelector('input[type="password"]').value
        };

        try {
            const response = await fetch('/login_user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const resData = await response.json();

            if (response.ok) {
                showToast(`Welcome back, ${resData.user}! Redirecting...`);
                toggleModal('authModal', 'close');
                
                // Redirect to dashboard module after short delay
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                showToast(resData.message);
            }
        } catch (error) {
            showToast("Server unreachable.");
        }
    });
}

// --- 7. Dashboard Data Fetching Module ---
async function loadDashboardData() {
    const bTable = document.querySelector('#bTable tbody');
    const iTable = document.querySelector('#iTable tbody');
    
    // Only run if we are actually on the dashboard page
    if (!bTable || !iTable) return;

    try {
        const response = await fetch('/get_user_data');
        const data = await response.json();

        // Populate Bookings Table
        data.bookings.forEach(b => {
            const row = `<tr>
                <td>${b.resource_id}</td>
                <td><span class="status-badge ${b.status.toLowerCase()}">${b.status}</span></td>
            </tr>`;
            bTable.innerHTML += row;
        });

        // Populate Issues Table
        data.issues.forEach(i => {
            const row = `<tr>
                <td>${i.description}</td>
                <td><span class="status-badge busy">${i.status}</span></td>
            </tr>`;
            iTable.innerHTML += row;
        });
    } catch (error) {
        console.error("Failed to load dashboard data");
    }
}

// Initialize dashboard if elements exist
document.addEventListener('DOMContentLoaded', loadDashboardData);

// --- 8. UI Feedback (Toast Notification) ---
function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}
