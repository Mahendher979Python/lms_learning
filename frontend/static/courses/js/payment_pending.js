/* ===================================
   RESPONSIVE PAYMENT PENDING JS
=================================== */

document.addEventListener("DOMContentLoaded", function(){

    // ==========================
    // BUTTON LOADING EFFECT
    // ==========================
    const form = document.querySelector("form");
    const button = document.querySelector("button");

    if(form){

        form.addEventListener("submit", function(){

            button.innerHTML = "⏳ Redirecting...";
            button.disabled = true;
            button.style.opacity = "0.8";

        });
    }

    // ==========================
    // ONLINE / OFFLINE STATUS
    // ==========================
    window.addEventListener("offline", function(){

        alert("⚠️ Internet connection lost!");
    });

    window.addEventListener("online", function(){

        console.log("Internet connection restored");
    });

    // ==========================
    // PAGE FADE EFFECT
    // ==========================
    document.body.style.opacity = "0";

    setTimeout(() => {

        document.body.style.transition = "opacity 0.5s ease";
        document.body.style.opacity = "1";

    }, 100);

});