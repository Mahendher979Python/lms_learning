// =========================
// CARD ANIMATION
// =========================

const cards = document.querySelectorAll(".certificate-card");

cards.forEach((card, index) => {

    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";

    setTimeout(() => {

        card.style.transition = "0.5s ease";

        card.style.opacity = "1";
        card.style.transform = "translateY(0px)";

    }, index * 150);

});

// =========================
// BUTTON CLICK EFFECT
// =========================

const buttons = document.querySelectorAll(
    ".view-btn, .download-btn"
);

buttons.forEach(btn => {

    btn.addEventListener("click", function(){

        this.style.transform = "scale(0.96)";

        setTimeout(() => {

            this.style.transform = "scale(1)";

        }, 150);

    });

});

// =========================
// MOBILE TOUCH FIX
// =========================

document.addEventListener(
    "touchstart",
    function(){},
    true
);