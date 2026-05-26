/* ===================================
   RESPONSIVE PAYMENT FAILED PAGE JS
=================================== */

document.addEventListener("DOMContentLoaded", function(){

    // ==========================
    // AUTO BUTTON EFFECT
    // ==========================
    const retryBtn = document.querySelector(".retry-btn");

    if(retryBtn){

        retryBtn.addEventListener("mouseenter", function(){

            this.style.transform = "translateY(-2px)";
        });

        retryBtn.addEventListener("mouseleave", function(){

            this.style.transform = "translateY(0)";
        });
    }

    // ==========================
    // NETWORK CHECK
    // ==========================
    window.addEventListener("offline", function(){

        alert("⚠️ Internet connection lost!");
    });

    // ==========================
    // PAGE LOAD EFFECT
    // ==========================
    document.body.style.opacity = "0";

    setTimeout(() => {

        document.body.style.transition = "opacity 0.4s ease";
        document.body.style.opacity = "1";

    }, 100);

});