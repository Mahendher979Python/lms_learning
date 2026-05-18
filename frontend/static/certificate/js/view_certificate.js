document.addEventListener("DOMContentLoaded", function () {

    /* ===== BUTTON CLICK EFFECT ===== */
    const buttons = document.querySelectorAll(".action-btn");

    buttons.forEach(btn => {

        btn.addEventListener("click", function () {

            this.style.transform = "scale(0.96)";

            setTimeout(() => {
                this.style.transform = "scale(1)";
            }, 120);

        });

    });

    /* ===== CERTIFICATE FADE ANIMATION ===== */
    const card = document.querySelector(".certificate-card") || document.querySelector(".certificate");

    if(card){

        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";

        setTimeout(() => {

            card.style.transition = "all 0.7s ease";

            card.style.opacity = "1";
            card.style.transform = "translateY(0)";

        }, 100);

    }

    /* ===== MOBILE TOUCH EFFECT ===== */
    if(window.innerWidth < 768){

        document.querySelectorAll(".photo-frame").forEach(frame => {

            frame.addEventListener("touchstart", function(){

                this.style.transform = "scale(1.03)";
                this.style.transition = "0.3s";

            });

            frame.addEventListener("touchend", function(){

                this.style.transform = "scale(1)";

            });

        });

    }

});
