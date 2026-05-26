let map;
let marker;
let chart;

let workStart = window.workStart || "";
let logoutTime = window.logoutTime || "";

let timerInterval;

let breakStart = null;
let breakInterval;

/* =========================
   INIT
========================= */

document.addEventListener("DOMContentLoaded", () => {

    startWorkTimer();

    if(document.getElementById("chart")){
        loadChart();
    }

    autoGPS();

});

/* =========================
   WORK TIMER
========================= */

function startWorkTimer(){

    if(!workStart) return;

    let start = new Date(workStart);

    timerInterval = setInterval(() => {

        let end = logoutTime
            ? new Date(logoutTime)
            : new Date();

        let diff = Math.floor((end - start) / 1000);

        if(diff < 0){
            diff = 0;
        }

        let h = Math.floor(diff / 3600);
        let m = Math.floor((diff % 3600) / 60);
        let s = diff % 60;

        document.getElementById("workTimer").innerHTML =
            `${String(h).padStart(2,'0')}:` +
            `${String(m).padStart(2,'0')}:` +
            `${String(s).padStart(2,'0')}`;

        if(logoutTime){
            clearInterval(timerInterval);
        }

    },1000);

}

/* =========================
   BREAK TIMER
========================= */

function startBreak(){

    fetch("/attendance/start-break/");

    breakStart = new Date();

    runBreakTimer();

}

function endBreak(){

    fetch("/attendance/end-break/");

    clearInterval(breakInterval);

    document.getElementById("breakTimer").innerHTML =
        "00:00:00";

}

function runBreakTimer(){

    breakInterval = setInterval(() => {

        let diff = Math.floor(
            (new Date() - breakStart) / 1000
        );

        let h = Math.floor(diff / 3600);
        let m = Math.floor((diff % 3600) / 60);
        let s = diff % 60;

        document.getElementById("breakTimer").innerHTML =
            `${String(h).padStart(2,'0')}:` +
            `${String(m).padStart(2,'0')}:` +
            `${String(s).padStart(2,'0')}`;

    },1000);

}

/* =========================
   FILTER TABLE
========================= */

function filterData(type){

    const rows = document.querySelectorAll(
        "#trainerAttendanceTable tr[data-date]"
    );

    const now = new Date();

    rows.forEach(row => {

        let rowDate = new Date(row.dataset.date);

        let diff =
            (now - rowDate) /
            (1000 * 60 * 60 * 24);

        let show = false;

        if(type === "day" && diff <= 1){
            show = true;
        }
        else if(type === "week" && diff <= 7){
            show = true;
        }
        else if(type === "month" && diff <= 30){
            show = true;
        }
        else if(type === "year" && diff <= 365){
            show = true;
        }
        else if(type === "all"){
            show = true;
        }

        row.style.display = show ? "" : "none";

    });

}

/* =========================
   SEARCH STUDENT
========================= */

function searchStudent(){

    let input = document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    let rows = document.querySelectorAll(
        "#studentTable tr"
    );

    rows.forEach((row,index) => {

        if(index === 0) return;

        let name = row
            .querySelector(".student-name")
            .innerText
            .toLowerCase();

        row.style.display =
            name.includes(input)
            ? ""
            : "none";

    });

}

/* =========================
   CHART
========================= */

function loadChart(){

    if(typeof chartLabels === "undefined") return;

    const ctx = document
        .getElementById("chart")
        .getContext("2d");

    chart = new Chart(ctx,{

        type:'line',

        data:{
            labels:chartLabels,

            datasets:[{
                label:'Working Hours',
                data:chartValues,
                borderColor:'#2563eb',
                borderWidth:3,
                tension:0.3,
                fill:false
            }]
        },

        options:{
            responsive:true,
            maintainAspectRatio:false,

            scales:{
                y:{
                    beginAtZero:true
                }
            }
        }

    });

}

/* =========================
   GOOGLE MAP
========================= */

function initMap(){

    map = new google.maps.Map(
        document.getElementById("map"),
        {
            zoom:5,
            center:{
                lat:20.5937,
                lng:78.9629
            }
        }
    );

    loadLocation();

}

function loadLocation(){

    fetch("/attendance/latest-location/")

    .then(res => res.json())

    .then(data => {

        if(data.lat && data.lng){

            const pos = {
                lat:parseFloat(data.lat),
                lng:parseFloat(data.lng)
            };

            if(marker){
                marker.setMap(null);
            }

            marker = new google.maps.Marker({
                position:pos,
                map:map
            });

            map.setCenter(pos);

            map.setZoom(15);

        }

    });

}

/* =========================
   AUTO GPS
========================= */

function autoGPS(){

    if(!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(pos => {

        fetch("/attendance/auto-location/",{

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

/* =========================
   CSRF
========================= */

function getCookie(name){

    let cookieValue = null;

    if(document.cookie){

        document.cookie.split(";").forEach(c => {

            c = c.trim();

            if(c.startsWith(name + "=")){

                cookieValue =
                    decodeURIComponent(
                        c.substring(name.length + 1)
                    );

            }

        });

    }

    return cookieValue;

}