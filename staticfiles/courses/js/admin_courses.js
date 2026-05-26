/* ===================================
   BUTTON CLICK EFFECT
=================================== */

document.querySelectorAll(".btn, .create-btn").forEach(button => {

    button.addEventListener("click", function(){

        this.style.transform = "scale(0.94)";

        setTimeout(() => {
            this.style.transform = "";
        }, 150);

    });

});

/* ===================================
   TABLE ROW HOVER EFFECT
=================================== */

document.querySelectorAll("tbody tr").forEach(row => {

    row.addEventListener("mouseenter", () => {

        row.style.transition = "0.3s";
        row.style.boxShadow =
        "0 10px 25px rgba(37,99,235,0.08)";

    });

    row.addEventListener("mouseleave", () => {

        row.style.boxShadow = "none";

    });

});

/* ===================================
   SEARCH INPUT EFFECT
=================================== */

const searchInput =
document.querySelector(".search-box input");

if(searchInput){

    searchInput.addEventListener("focus", () => {

        searchInput.style.transform = "scale(1.01)";

    });

    searchInput.addEventListener("blur", () => {

        searchInput.style.transform = "scale(1)";

    });

}

/* ===================================
   MOBILE TOUCH EFFECT
=================================== */

if(window.innerWidth <= 768){

    document.querySelectorAll("tbody tr").forEach(card => {

        card.addEventListener("touchstart", () => {

            card.style.transform = "scale(0.98)";

        });

        card.addEventListener("touchend", () => {

            card.style.transform = "scale(1)";

        });

    });

}

/* ===================================
   TABLE LOAD ANIMATION
=================================== */

document.querySelectorAll("tbody tr").forEach((row,index)=>{

    row.style.opacity = "0";
    row.style.transform = "translateY(20px)";

    setTimeout(()=>{

        row.style.transition = "0.4s ease";
        row.style.opacity = "1";
        row.style.transform = "translateY(0)";

    }, index * 80);

});