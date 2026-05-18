/* =========================
   TRAINER DASHBOARD JS
========================= */

document.addEventListener("DOMContentLoaded", () => {

    animateProgressBars();

    initCharts();

    initCardHover();

});

/* =========================
   PROGRESS BAR ANIMATION
========================= */

function animateProgressBars(){

    const bars = document.querySelectorAll(".progress-fill");

    bars.forEach(bar => {

        const width =
            bar.getAttribute("data-width") || 0;

        setTimeout(() => {

            bar.style.width = width + "%";

        }, 300);

    });

}

/* =========================
   CARD ANIMATION
========================= */

function initCardHover(){

    const cards = document.querySelectorAll(".card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.boxShadow =
                "0 12px 30px rgba(37,99,235,0.15)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.boxShadow =
                "0 6px 18px rgba(15,23,42,0.08)";

        });

    });

}

/* =========================
   SAFE JSON DATA
========================= */

const courses =
JSON.parse(
    document.getElementById("courses-data").textContent
);

const topics =
JSON.parse(
    document.getElementById("topics-data").textContent
);

const assignments =
JSON.parse(
    document.getElementById("assignments-data").textContent
);

/* =========================
   CHARTS
========================= */

function initCharts(){

    /* BAR CHART */

    const trainerCtx =
    document.getElementById("trainerChart");

    if(trainerCtx){

        new Chart(trainerCtx, {

            type: "bar",

            data: {

                labels: [
                    "Courses",
                    "Topics",
                    "Assignments"
                ],

                datasets: [{

                    label: "Trainer Stats",

                    data: [
                        courses,
                        topics,
                        assignments
                    ],

                    backgroundColor: [
                        "#2563eb",
                        "#16a34a",
                        "#f59e0b"
                    ],

                    borderRadius: 10,
                    borderWidth: 0

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
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

    /* DOUGHNUT CHART */

    const studentCtx =
    document.getElementById("studentChart");

    if(studentCtx){

        new Chart(studentCtx, {

            type: "doughnut",

            data: {

                labels: [
                    "Completed",
                    "Pending",
                    "Not Started"
                ],

                datasets: [{

                    data: [65,25,10],

                    backgroundColor: [
                        "#16a34a",
                        "#f59e0b",
                        "#ef4444"
                    ],

                    borderWidth: 0

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        });

    }

}

/* =========================
   RESPONSIVE TABLE SCROLL
========================= */

window.addEventListener("resize", () => {

    const tableBox =
    document.querySelector(".table-box");

    if(window.innerWidth < 768){

        tableBox.style.overflowX = "auto";

    }else{

        tableBox.style.overflowX = "visible";

    }

});