/* =========================
   CREATE BATCH JS
========================= */

document.addEventListener("DOMContentLoaded", function(){

    animateForm();

    inputEffects();

    formValidation();

});

/* =========================
   FORM ENTRY ANIMATION
========================= */

function animateForm(){

    const card =
    document.querySelector(".batch-card");

    if(card){

        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";

        setTimeout(()=>{

            card.style.transition =
                "all 0.5s ease";

            card.style.opacity = "1";
            card.style.transform =
                "translateY(0)";

        },200);

    }

}

/* =========================
   INPUT EFFECTS
========================= */

function inputEffects(){

    const fields =
    document.querySelectorAll(
        "input, select, textarea"
    );

    fields.forEach(field=>{

        field.addEventListener("focus", ()=>{

            field.style.background =
            "#f8fbff";

        });

        field.addEventListener("blur", ()=>{

            field.style.background =
            "#fff";

        });

    });

}

/* =========================
   SIMPLE VALIDATION
========================= */

function formValidation(){

    const form =
    document.querySelector("form");

    const button =
    document.querySelector(".submit-btn");

    if(!form || !button) return;

    form.addEventListener("submit", function(e){

        const inputs =
        form.querySelectorAll(
            "input, select, textarea"
        );

        let valid = true;

        inputs.forEach(input=>{

            if(
                input.hasAttribute("required") &&
                !input.value.trim()
            ){

                valid = false;

                input.style.borderColor =
                "#ef4444";

            }else{

                input.style.borderColor =
                "#dbe2ea";

            }

        });

        if(!valid){

            e.preventDefault();

            alert(
                "Please fill all required fields"
            );

            return;
        }

        /* BUTTON LOADING */

        button.innerHTML =
        "Creating Batch...";

        button.disabled = true;

    });

}

/* =========================
   RESPONSIVE FIX
========================= */

window.addEventListener("resize", ()=>{

    const card =
    document.querySelector(".batch-card");

    if(window.innerWidth < 480){

        card.style.maxWidth = "100%";

    }else{

        card.style.maxWidth = "480px";

    }

});