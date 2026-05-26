document.addEventListener("DOMContentLoaded", function(){

    // FORM
    const form = document.getElementById("certificateForm");

    // BUTTON
    const submitBtn = document.getElementById("submitBtn");

    // SUCCESS
    const successMessage =
    document.getElementById("successMessage");

    // FILE INPUT EFFECT
    document.querySelectorAll('input[type="file"]')
    .forEach(input => {

        input.addEventListener("change", function(){

            if(this.files.length > 0){

                this.style.borderColor = "#16a34a";

            }

        });

    });

    // FORM SUBMIT EFFECT
    if(form){

        form.addEventListener("submit", function(){

            submitBtn.innerHTML =
            "Sending...";

            submitBtn.disabled = true;

            setTimeout(() => {

                successMessage.style.display =
                "block";

            }, 1000);

        });

    }

    // AUTO FOCUS
    const firstInput =
    document.querySelector("input, textarea, select");

    if(firstInput){
        firstInput.focus();
    }

});