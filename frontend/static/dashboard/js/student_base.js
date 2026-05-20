function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("closed");
    document.getElementById("main").classList.toggle("full");
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        if (navbar.style.left === "260px") {
            navbar.style.left = "0px";
        } else {
            navbar.style.left = "260px";
        }
    }
}

function toggleDark() {
    const isDark = document.body.classList.toggle("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
}

/* NOTIFICATIONS (FIXED + SAFE) */
function loadNotifications() {
    fetch("/notifications/")
    .then(res => res.json())
    .then(data => {

        const dropdown = document.getElementById("dropdown");
        const count = document.getElementById("count");

        dropdown.innerHTML = "";
        count.innerText = data.unread_count || 0;

        if (!data.notifications || data.notifications.length === 0) {
            dropdown.innerHTML = "<div style='padding:10px;'>No notifications</div>";
            return;
        }

        data.notifications.forEach(n => {
            let div = document.createElement("div");

            div.className = "notif-item " + (n.type || "");

            div.innerHTML = `
                <b>${n.type ? n.type.toUpperCase() : "INFO"}</b><br>
                ${n.message || ""}<br>
                <small>${n.course || ""}</small><br>
                <small style="color:gray">${n.time || ""}</small>
            `;

            div.onclick = function () {
                fetch(`/notifications/read/${n.id}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    }
                });
                div.style.opacity = "0.5";
            };

            dropdown.appendChild(div);
        });
    });
}

/* dropdown toggle */
document.addEventListener("DOMContentLoaded", function () {

    const box = document.getElementById("notifBox");
    const dropdown = document.getElementById("dropdown");

    box.addEventListener("click", function (e) {
        dropdown.style.display =
            dropdown.style.display === "block" ? "none" : "block";
        e.stopPropagation();
    });

    document.addEventListener("click", function () {
        dropdown.style.display = "none";
    });

    loadNotifications();
    setInterval(loadNotifications, 5000);
});

/* CSRF */
function getCookie(name) {
    let cookieValue = null;
    document.cookie.split(";").forEach(c => {
        c = c.trim();
        if (c.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(c.substring(name.length + 1));
        }
    });
    return cookieValue;
}

/* 3D LOGOUT MODAL ACTION HANDLERS */
function showLogoutModal(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    const modal = document.getElementById("logout-confirm-modal");
    if (modal) {
        modal.classList.add("active");
    }
}

function closeLogoutModal() {
    const modal = document.getElementById("logout-confirm-modal");
    if (modal) {
        modal.classList.remove("active");
    }
}

function confirmLogout() {
    const form = document.getElementById("logout-post-form");
    if (form) {
        form.submit();
    } else {
        // Fallback to simple redirect if form is not found
        window.location.href = "/en/logout/";
    }
}
