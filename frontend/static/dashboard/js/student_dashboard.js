// document.querySelectorAll(".progress-fill").forEach(el => {

//     let val = el.getAttribute("data-progress") || 0;

//     el.style.width = val + "%";

// });
/* =======================
   PROGRESS ANIMATION
======================= */

document.addEventListener("DOMContentLoaded", function(){

    const progressBars =
        document.querySelectorAll(".progress-fill");

    progressBars.forEach(function(bar){

        const progress =
            bar.getAttribute("data-progress");

        setTimeout(function(){

            bar.style.width = progress + "%";

        },300);

    });

});

/* =======================
   CARD HOVER EFFECT
======================= */

const cards =
document.querySelectorAll(
".stat-card,.course,.card"
);

cards.forEach(function(card){

    card.addEventListener("mousemove", function(e){

        const rect =
        card.getBoundingClientRect();

        const x =
        e.clientX - rect.left;

        const y =
        e.clientY - rect.top;

        const rotateX =
        ((y / rect.height)-0.5)*6;

        const rotateY =
        ((x / rect.width)-0.5)*-6;

        card.style.transform =
        `perspective(1000px)
        rotateX(${rotateX}deg)
        rotateY(${rotateY}deg)
        translateY(-4px)`;

    });

    card.addEventListener("mouseleave", function(){

        card.style.transform =
        "perspective(1000px) rotateX(0) rotateY(0)";

    });

});