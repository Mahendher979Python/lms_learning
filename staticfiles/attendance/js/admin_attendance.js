/* =========================
   SAFE DJANGO CHART DATA
========================= */

const labels = JSON.parse('{{ dates|escapejs }}');
const values = JSON.parse('{{ hours|escapejs }}');

/* =========================
   CHART JS
========================= */

document.addEventListener("DOMContentLoaded", function(){

    const chartCanvas = document.getElementById("chart");

    if(chartCanvas){

        new Chart(chartCanvas, {

            type: 'line',

            data: {

                labels: labels,

                datasets: [{

                    label: 'Working Hours',

                    data: values,

                    borderColor: '#2563eb',

                    backgroundColor: 'rgba(37,99,235,0.1)',

                    borderWidth: 3,

                    tension: 0.4,

                    fill: true,

                    pointRadius: 5,

                    pointHoverRadius: 7

                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: true,
                        position: 'top'
                    }

                },

                scales: {

                    y: {
                        beginAtZero: true
                    }

                }

            }

        });

    }

});

/* =========================
   GOOGLE MAP
========================= */

let map;
let marker;

async function initMap() {

    const defaultLocation = {
        lat: 17.3850,
        lng: 78.4867
    };

    const { Map } =
        await google.maps.importLibrary("maps");

    const { AdvancedMarkerElement } =
        await google.maps.importLibrary("marker");

    map = new Map(document.getElementById("map"), {

        zoom: 10,

        center: defaultLocation,

        mapId: "DEMO_MAP_ID",

        gestureHandling: "greedy"

    });

    marker = new AdvancedMarkerElement({

        map: map,

        position: defaultLocation,

        title: "Default Location"

    });

    /* =========================
       TABLE ROW CLICK
    ========================= */

    document.querySelectorAll(".row-map").forEach(row => {

        row.addEventListener("click", () => {

            const lat = row.dataset.lat;
            const lng = row.dataset.lng;
            const user = row.dataset.user;

            if(!lat || !lng){

                showToast("Location not available");
                return;
            }

            const position = {

                lat: parseFloat(lat),

                lng: parseFloat(lng)

            };

            map.setCenter(position);

            map.setZoom(16);

            marker.position = position;

            marker.title = user;

            highlightRow(row);

        });

    });

}

/* =========================
   ROW HIGHLIGHT
========================= */

function highlightRow(selectedRow){

    document.querySelectorAll(".row-map").forEach(row => {

        row.classList.remove("active-row");

    });

    selectedRow.classList.add("active-row");

}

/* =========================
   MOBILE TOAST
========================= */

function showToast(message){

    let toast = document.createElement("div");

    toast.innerHTML = message;

    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.background = "#2563eb";
    toast.style.color = "white";
    toast.style.padding = "12px 18px";
    toast.style.borderRadius = "10px";
    toast.style.zIndex = "9999";
    toast.style.fontSize = "14px";
    toast.style.boxShadow = "0 4px 12px rgba(0,0,0,0.2)";

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.remove();

    }, 2500);

}

/* =========================
   RESPONSIVE MAP RESIZE
========================= */

window.addEventListener("resize", () => {

    if(map){

        google.maps.event.trigger(map, "resize");

    }

});

/* =========================
   EXPORT MAP INIT
========================= */

window.initMap = initMap;