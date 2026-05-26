

const notifBox =
document.getElementById("notifBox");

const dropdown =
document.getElementById("dropdown");

const count =
document.getElementById("count");


function loadNotifications(){

    fetch("/notifications/")

    .then(res => res.json())

    .then(data => {

        count.innerText =
            data.unread_count;

        let html = "";

        if(data.notifications.length === 0){

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


notifBox.addEventListener("click", () => {

    if(dropdown.style.display === "block"){

        dropdown.style.display = "none";

    }else{

        dropdown.style.display = "block";

    }

});


loadNotifications();

setInterval(loadNotifications, 10000);

