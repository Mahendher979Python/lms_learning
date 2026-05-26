document.addEventListener("DOMContentLoaded", () => {

    // BUTTON CLICK EFFECT
    const buttons = document.querySelectorAll(".btn");

    buttons.forEach(btn => {

        btn.addEventListener("click", function(e){

            // APPROVE CONFIRM
            if(this.classList.contains("btn-success")){

                const ok = confirm(
                    "Approve this certificate request?"
                );

                if(!ok){
                    e.preventDefault();
                }
            }

            // REJECT CONFIRM
            if(this.classList.contains("btn-danger")){

                const ok = confirm(
                    "Reject this certificate request?"
                );

                if(!ok){
                    e.preventDefault();
                }
            }

        });

    });

    // MOBILE TABLE SCROLL SHADOW
    const tableWrapper = document.querySelector(".table-wrapper");

    if(tableWrapper){

        tableWrapper.addEventListener("scroll", () => {

            if(tableWrapper.scrollLeft > 0){

                tableWrapper.style.boxShadow =
                    "inset 10px 0 10px -10px rgba(0,0,0,0.15)";

            }else{

                tableWrapper.style.boxShadow = "none";

            }

        });

    }

});