

const notifBox = document.getElementById("notifBox");
const dropdown = document.getElementById("dropdown");
const count = document.getElementById("count") || document.getElementById("notif-count");


function loadNotifications(){

    fetch("/notifications/")

    .then(res => res.json())

    .then(data => {

        if (count) {
            count.innerText = data.unread_count || 0;
        }

        // If this page doesn't render a dropdown list, nothing else to do.
        if (!dropdown) return;

        let html = "";

        if(!data.notifications || data.notifications.length === 0){

            html =
            `<div class="dropdown-item">
                No Notifications
            </div>`;

        }else{

            data.notifications.forEach(n => {

                html += `

                <div class="dropdown-item">

                    <div>
                        ${n.message}
                    </div>

                    <div class="dropdown-time">
                        ${n.time}
                    </div>

                </div>

                `;

            });

        }

        html += `

        <div class="dropdown-item"
             style="text-align:center;">

            <a href="/notifications/page/">
                View All
            </a>

        </div>
        `;

        dropdown.innerHTML = html;

    });

}


if (notifBox && dropdown) {
notifBox.addEventListener("click", () => {

    if(dropdown.style.display === "block"){

        dropdown.style.display = "none";

    }else{

        dropdown.style.display = "block";

    }

});
}


loadNotifications();

setInterval(loadNotifications, 10000);

