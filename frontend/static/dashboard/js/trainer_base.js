// Trainer dashboard JS - Fully Responsive
let sidebarState = localStorage.getItem('sidebarState') || 'expanded';

function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    
    if (window.innerWidth >= 768 && sidebarState === 'collapsed') {
        sidebar.classList.add('collapsed');
    } else if (window.innerWidth < 768) {
        sidebar.classList.add('closed');
    }
}

function syncSidebarLayout() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const navbar = document.querySelector('.navbar');

    if (!sidebar) return;

    const isMobile = window.innerWidth < 768;

    if (isMobile) {
        if (!sidebar.classList.contains('closed')) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    } else {
        overlay.classList.remove('active');
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    if (window.innerWidth < 768) {
        sidebar.classList.toggle('closed');
    } else {
        sidebar.classList.toggle('collapsed');
        
        sidebarState = sidebar.classList.contains('collapsed') ? 'collapsed' : 'expanded';
        localStorage.setItem('sidebarState', sidebarState);
    }
    
    syncSidebarLayout();
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (sidebar) sidebar.classList.add('closed');
    if (overlay) overlay.classList.remove('active');
    syncSidebarLayout();
}

function toggleDark() {
    const currentTheme = document.body.classList.contains('light') ? 'light' : 
                         document.body.classList.contains('darth') ? 'darth' : 'dark';
    
    // Cycle through themes: dark → light → darth → dark
    let newTheme;
    if (currentTheme === 'dark') {
        newTheme = 'light';
    } else if (currentTheme === 'light') {
        newTheme = 'darth';
    } else {
        newTheme = 'dark';
    }

    // Remove all theme classes
    document.body.classList.remove('light', 'darth');
    
    // Add new theme class if not dark
    if (newTheme === 'light') {
        document.body.classList.add('light');
    } else if (newTheme === 'darth') {
        document.body.classList.add('darth');
    }

    localStorage.setItem('theme', newTheme);

    const darkModeCheckbox = document.querySelector('input[name="dark_mode"]');
    if (darkModeCheckbox) {
        darkModeCheckbox.checked = (newTheme === 'dark' || newTheme === 'darth');
    }

    if (window.TOGGLE_THEME_API) {
        fetch(`${window.TOGGLE_THEME_API}?theme=${newTheme}`)
            .catch(err => console.error('Theme sync error:', err));
    }
}

function loadNotifications() {
    const url = window.NOTIFICATIONS_API || '/notifications/';
    fetch(url)
        .then(res => res.json())
        .then(data => {
            const badge = document.getElementById('notif-count');
            if (!badge) return;

            const unread = data && typeof data.unread_count === 'number' ? data.unread_count : 0;
            badge.innerText = unread;
            badge.style.display = unread > 0 ? 'flex' : 'none';
        })
        .catch(err => console.error('Notification load error:', err));
}

function showLogoutModal(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    const modal = document.getElementById('logout-confirm-modal');
    if (modal) modal.classList.add('active');
}

function closeLogoutModal() {
    const modal = document.getElementById('logout-confirm-modal');
    if (modal) modal.classList.remove('active');
}

function confirmLogout() {
    const form = document.getElementById('logout-post-form');
    if (form) {
        form.submit();
    } else {
        window.location.href = '/en/logout/';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Initialize theme from localStorage or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.classList.remove('light', 'darth');
    if (savedTheme === 'light') {
        document.body.classList.add('light');
    } else if (savedTheme === 'darth') {
        document.body.classList.add('darth');
    }
    
    initSidebar();
    syncSidebarLayout();
    loadNotifications();
    setInterval(loadNotifications, 5000);
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeLogoutModal();
            if (window.innerWidth < 768) {
                closeSidebar();
            }
        }
    });

    const darkModeCheckbox = document.querySelector('input[name="dark_mode"]');
    if (darkModeCheckbox) {
        darkModeCheckbox.checked = (savedTheme === 'dark' || savedTheme === 'darth');
        darkModeCheckbox.addEventListener('change', () => {
            const currentTheme = document.body.classList.contains('light') ? 'light' : 
                                 document.body.classList.contains('darth') ? 'darth' : 'dark';
            const checkboxIsChecked = darkModeCheckbox.checked;
            
            if (!checkboxIsChecked && currentTheme === 'light') {
                toggleDark();
            } else if (checkboxIsChecked && currentTheme === 'darth') {
                // Already dark/darth
            } else if (!checkboxIsChecked && currentTheme === 'dark') {
                // Already dark/darth
            } else if (!checkboxIsChecked) {
                // Already dark/darth
            } else {
                // If unchecking and currently darth/dark, set to light
                if (currentTheme !== 'light') {
                    toggleDark();
                }
            }
        });
    }
});

window.addEventListener('resize', () => {
    syncSidebarLayout();
    
    if (window.innerWidth >= 768) {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            if (sidebarState === 'collapsed') {
                sidebar.classList.add('collapsed');
                sidebar.classList.remove('closed');
            } else {
                sidebar.classList.remove('collapsed');
                sidebar.classList.remove('closed');
            }
        }
    } else {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.add('closed');
            sidebar.classList.remove('collapsed');
        }
    }
});
