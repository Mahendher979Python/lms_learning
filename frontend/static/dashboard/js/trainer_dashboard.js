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
   CHARTS
========================= */

function initCharts(){

    let courses = 0;
    let topics = 0;
    let assignments = 0;

    const coursesDataEl = document.getElementById('courses-data');
    const topicsDataEl = document.getElementById('topics-data');
    const assignmentsDataEl = document.getElementById('assignments-data');

    if (coursesDataEl) {
        try {
            courses = JSON.parse(coursesDataEl.textContent);
        } catch (e) {
            console.error('Error parsing courses data:', e);
        }
    }

    if (topicsDataEl) {
        try {
            topics = JSON.parse(topicsDataEl.textContent);
        } catch (e) {
            console.error('Error parsing topics data:', e);
        }
    }

    if (assignmentsDataEl) {
        try {
            assignments = JSON.parse(assignmentsDataEl.textContent);
        } catch (e) {
            console.error('Error parsing assignments data:', e);
        }
    }

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