// Dashboard base JS (used by frontend/templates/dashboard/base.html)
// Purpose: provide stable sidebar/theme/notifications/logout behaviour.

function syncSidebarLayout() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebar-overlay");
    const navbar = document.querySelector(".navbar");

    if (!sidebar) return;

    const isMobile = window.innerWidth <= 768;
    const isClosed = sidebar.classList.contains("closed");

    // Overlay only matters on mobile.
    if (overlay) {
        if (isMobile && !isClosed) overlay.classList.add("active");
        else overlay.classList.remove("active");
    }

    // Force navbar flush-left on mobile.
    if (navbar && isMobile) navbar.style.left = "0px";
    else if (navbar) navbar.style.left = "";
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");
    if (!sidebar) return;

    sidebar.classList.toggle("closed");
    if (main) main.classList.toggle("full");
    syncSidebarLayout();
}

function closeSidebar() {
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");
    const overlay = document.getElementById("sidebar-overlay");

    if (sidebar) sidebar.classList.add("closed");
    if (main) main.classList.add("full");
    if (overlay) overlay.classList.remove("active");
    syncSidebarLayout();
}

function toggleDark() {
    const isDark = document.body.classList.toggle("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
}

function loadNotifications() {
    const url = (window.NOTIFICATIONS_API || "/notifications/");
    fetch(url)
        .then(res => res.json())
        .then(data => {
            const badge = document.getElementById("notif-count");
            if (!badge) return;

            const unread = data && typeof data.unread_count === "number" ? data.unread_count : 0;
            badge.innerText = unread;
            badge.style.display = unread > 0 ? "flex" : "none";
        })
        .catch(() => { });
}

function showLogoutModal(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    const modal = document.getElementById("logout-confirm-modal");
    if (modal) modal.classList.add("active");
}

function closeLogoutModal() {
    const modal = document.getElementById("logout-confirm-modal");
    if (modal) modal.classList.remove("active");
}

function confirmLogout() {
    const form = document.getElementById("logout-post-form");
    if (form) form.submit();
    else window.location.href = "/en/logout/";
}

document.addEventListener("DOMContentLoaded", function () {
    syncSidebarLayout();
    loadNotifications();
    setInterval(loadNotifications, 5000);
});

window.addEventListener("resize", syncSidebarLayout);
