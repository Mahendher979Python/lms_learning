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

/* TOGGLE DROPDOWN */
function toggleDropdown(e) {
    e.stopPropagation();
    let d = document.getElementById("dropdown");
    d.style.display = (d.style.display === "block") ? "none" : "block";
}

/* CLOSE OUTSIDE */
document.addEventListener("click", function () {
    document.getElementById("dropdown").style.display = "none";
});

/* LOAD NOTIFICATIONS */
function loadNotifications() {
    fetch("/notifications/")
    .then(res => res.json())
    .then(data => {

        let dropdown = document.getElementById("dropdown");
        let count = document.getElementById("count");

        dropdown.innerHTML = "";
        count.innerText = data.unread_count;

        if (data.notifications.length === 0) {
            dropdown.innerHTML = "<div style='padding:10px;'>No notifications</div>";
            return;
        }

        data.notifications.forEach(n => {
            let div = document.createElement("div");

            div.className = "notif-item " + n.type;

            div.innerHTML = `
                <b>${n.type.toUpperCase()}</b><br>
                ${n.message}<br>
                <small>${n.course || ""}</small><br>
                <small style="color:gray">${n.time}</small>
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

setInterval(loadNotifications, 5000);
loadNotifications();

/* CSRF */
function getCookie(name) {
    let cookieValue = null;
    document.cookie.split(';').forEach(c => {
        c = c.trim();
        if (c.startsWith(name + '=')) {
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
