/* =========================
   TEAMS / CLASSES JS
========================= */

document.addEventListener("DOMContentLoaded", function(){

    animateRows();

    animateButtons();

    responsiveTable();

});

/* =========================
   TABLE ROW ANIMATION
========================= */

function animateRows(){

    const rows =
    document.querySelectorAll(".team-table tbody tr");

    rows.forEach((row,index)=>{

        row.style.opacity = "0";

        row.style.transform = "translateY(20px)";

        setTimeout(()=>{

            row.style.transition =
                "all 0.5s ease";

            row.style.opacity = "1";

            row.style.transform =
                "translateY(0)";

        }, index * 120);

    });

}

/* =========================
   BUTTON EFFECTS
========================= */

function animateButtons(){

    const buttons =
    document.querySelectorAll(
        ".create-btn, .open-btn"
    );

    buttons.forEach(btn=>{

        btn.addEventListener("mouseenter", ()=>{

            btn.style.boxShadow =
            "0 8px 18px rgba(0,0,0,0.15)";

        });

        btn.addEventListener("mouseleave", ()=>{

            btn.style.boxShadow = "none";

        });

    });

}

/* =========================
   RESPONSIVE TABLE
========================= */

function responsiveTable(){

    const wrapper =
    document.querySelector(".table-wrapper");

    if(window.innerWidth < 768){

        wrapper.style.overflowX = "auto";

    }else{

        wrapper.style.overflowX = "visible";

    }

}

window.addEventListener(
    "resize",
    responsiveTable
);

/* =========================
   BUTTON CLICK EFFECT
========================= */

document.querySelectorAll(".open-btn")
.forEach(button=>{

    button.addEventListener("click", ()=>{

        button.innerHTML = "Opening...";

    });

});