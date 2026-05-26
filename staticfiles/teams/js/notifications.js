/* =========================
   NOTIFICATIONS JS
========================= */

document.addEventListener("DOMContentLoaded", function(){

    animateNotifications();

    backButtonEffect();

    autoHideEmptyMessage();

});

/* =========================
   ANIMATE NOTIFICATION BOXES
========================= */

function animateNotifications(){

    const notes =
    document.querySelectorAll(".note");

    notes.forEach((note,index)=>{

        note.style.opacity = "0";
        note.style.transform =
        "translateY(20px)";

        setTimeout(()=>{

            note.style.transition =
            "all 0.5s ease";

            note.style.opacity = "1";

            note.style.transform =
            "translateY(0)";

        }, index * 120);

    });

}

/* =========================
   BACK BUTTON EFFECT
========================= */

function backButtonEffect(){

    const backBtn =
    document.querySelector(".back");

    if(!backBtn) return;

    backBtn.addEventListener("mouseenter", ()=>{

        backBtn.style.transform =
        "translateX(-5px)";

    });

    backBtn.addEventListener("mouseleave", ()=>{

        backBtn.style.transform =
        "translateX(0px)";

    });

}

/* =========================
   EMPTY MESSAGE EFFECT
========================= */

function autoHideEmptyMessage(){

    const empty =
    document.querySelector(".empty");

    if(empty){

        empty.style.opacity = "0";

        setTimeout(()=>{

            empty.style.transition =
            "opacity 0.6s ease";

            empty.style.opacity = "1";

        },300);

    }

}

/* =========================
   CLICK EFFECT
========================= */

document.querySelectorAll(".note")
.forEach(note=>{

    note.addEventListener("click", ()=>{

        note.style.background =
        "#eff6ff";

        note.style.borderLeft =
        "5px solid #2563eb";

    });

});

/* =========================
   MOBILE RESPONSIVE FIX
========================= */

window.addEventListener("resize", ()=>{

    const box =
    document.querySelector(".box");

    if(window.innerWidth < 480){

        box.style.padding = "15px";

    }else{

        box.style.padding = "25px";

    }

});