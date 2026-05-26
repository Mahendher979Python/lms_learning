let map;
let marker;
let chart;

let workStart = "{{ today_login_time|default:'' }}";

let logoutTime = "{{ today_logout_time|default:'' }}";

let timerInterval;

let breakStart = null;
let breakInterval;

/* INIT */
document.addEventListener("DOMContentLoaded", function(){

    video = document.getElementById("video");

    startWorkTimer();

    autoGPS();

    loadChart();

    
});

/* WORK TIMER */
function startWorkTimer(){

    if(!workStart) return;

    let start = new Date(workStart);

    timerInterval = setInterval(function(){

        let endTime = logoutTime
            ? new Date(logoutTime)
            : new Date();

        let diff = Math.floor((endTime - start)/1000);

        if(diff < 0) diff = 0;

        let h = Math.floor(diff / 3600);
        let m = Math.floor((diff % 3600)/60);
        let s = diff % 60;

        document.getElementById("workTimer").innerHTML =
            String(h).padStart(2,'0') + ":" +
            String(m).padStart(2,'0') + ":" +
            String(s).padStart(2,'0');

        if(logoutTime){
            clearInterval(timerInterval);
        }

    },1000);
}

/* BREAK */
function startBreak(){

    fetch("{% url 'start_break' %}");

    breakStart = new Date();

    runBreakTimer();
}

function endBreak(){

    fetch("{% url 'end_break' %}");

    clearInterval(breakInterval);

    document.getElementById("breakTimer").innerHTML =
        "00:00:00";
}

function runBreakTimer(){

    breakInterval = setInterval(function(){

        let diff = Math.floor(
            (new Date() - breakStart)/1000
        );

        let h = Math.floor(diff/3600);
        let m = Math.floor((diff%3600)/60);
        let s = diff%60;

        document.getElementById("breakTimer").innerHTML =
            String(h).padStart(2,'0') + ":" +
            String(m).padStart(2,'0') + ":" +
            String(s).padStart(2,'0');

    },1000);
}

/* =========================
   CHART
========================= */

function loadChart() {

    let labels = JSON.parse('{{ dates|escapejs }}');
    let values = JSON.parse('{{ hours|escapejs }}');

    let ctx = document.getElementById('chart').getContext('2d');

    chart = new Chart(ctx, {

        type: 'line',

        data: {
            labels: labels,

            datasets: [{
                label: 'Working Hours',
                data: values,
                borderWidth: 3,
                tension: 0.3,
                fill: false
            }]
        },

        options: {
            responsive: true,

            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
/* MAP */
function initMap(){

    map = new google.maps.Map(
        document.getElementById("map"),
        {
            zoom:5,
            center:{lat:20.5937,lng:78.9629}
        }
    );
}

function showRowMap(row){

    let lat = parseFloat(row.dataset.lat);
    let lng = parseFloat(row.dataset.lng);

    if(!lat || !lng){
        alert("No location data");
        return;
    }

    let location = {lat:lat,lng:lng};

    map.setCenter(location);

    map.setZoom(15);

    if(marker){
        marker.setMap(null);
    }

    marker = new google.maps.Marker({
        position:location,
        map:map
    });
}

/* FILTER */
function filterData(type){

    let rows =
    document.querySelectorAll("#attendanceTable tr[data-date]");

    let now = new Date();

    rows.forEach(row=>{

        let diff =
        (now - new Date(row.dataset.date))
        /(1000*60*60*24);

        row.style.display =
            (type=='day' && diff<=1) ||
            (type=='week' && diff<=7) ||
            (type=='month' && diff<=30) ||
            (type=='year' && diff<=365)
            ? ""
            : "none";

    });
}

/* GPS */
function autoGPS(){

    if(!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(pos=>{

        fetch("{% url 'auto_location' %}",{

            method:"POST",

            headers:{
                "Content-Type":"application/json",
                "X-CSRFToken":getCookie("csrftoken")
            },

            body:JSON.stringify({
                lat:pos.coords.latitude,
                lng:pos.coords.longitude
            })

        });

    });

}



/* CSRF */
function getCookie(name){

    let cookieValue = null;

    document.cookie.split(";").forEach(c=>{

        c = c.trim();

        if(c.startsWith(name + "=")){

            cookieValue =
            decodeURIComponent(
                c.substring(name.length+1)
            );

        }

    });

    return cookieValue;
}

