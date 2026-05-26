/* =========================
   COURSE TEAMS JS
========================= */

document.addEventListener("DOMContentLoaded", function(){

    animateCards();

    hoverEffects();

    responsiveFix();

});

/* =========================
   CARD ENTRY ANIMATION
========================= */

function animateCards(){

    const cards =
    document.querySelectorAll(".course-card");

    cards.forEach((card,index)=>{

        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";

        setTimeout(()=>{

            card.style.transition =
                "all 0.5s ease";

            card.style.opacity = "1";
            card.style.transform =
                "translateY(0)";

        }, index * 120);

    });

}

/* =========================
   HOVER EFFECTS
========================= */

function hoverEffects(){

    const cards =
    document.querySelectorAll(".course-card");

    cards.forEach(card=>{

        card.addEventListener("mouseenter", ()=>{

            card.style.boxShadow =
            "0 15px 35px rgba(37,99,235,0.2)";

        });

        card.addEventListener("mouseleave", ()=>{

            card.style.boxShadow =
            "0 6px 20px rgba(0,0,0,0.08)";

        });

    });

}

/* =========================
   RESPONSIVE FIX
========================= */

function responsiveFix(){

    const grid =
    document.querySelector(".course-grid");

    if(window.innerWidth < 768){

        grid.style.gridTemplateColumns = "1fr";

    }else{

        grid.style.gridTemplateColumns =
        "repeat(auto-fit,minmax(280px,1fr))";

    }

}

window.addEventListener(
    "resize",
    responsiveFix
);

/* =========================
   CLICK EFFECT
========================= */

document.querySelectorAll(".course-link")
.forEach(link=>{

    link.addEventListener("click", function(){

        const footer =
        this.querySelector(".card-footer");

        footer.innerHTML =
        "Opening Teams...";

    });

});