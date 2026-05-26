/* ===============================
   RESPONSIVE CREATE COURSE JS
=================================*/

document.addEventListener("DOMContentLoaded", function(){

    // =========================
    // AUTO FOCUS
    // =========================
    const firstInput = document.querySelector(
        'input:not([type="hidden"]), textarea'
    );

    if(firstInput){
        firstInput.focus();
    }

    // =========================
    // PRICE VALIDATION
    // =========================
    const priceInput = document.getElementById("priceInput");

    if(priceInput){

        priceInput.addEventListener("input", function(){

            // Prevent negative
            if(parseFloat(this.value) < 0){
                this.value = 0;
            }

            // Limit decimals
            if(this.value.includes(".")){

                let parts = this.value.split(".");

                parts[1] = parts[1].slice(0,2);

                this.value = parts.join(".");
            }
        });
    }

    // =========================
    // FORM VALIDATION
    // =========================
    const form = document.getElementById("courseForm");

    if(form){

        form.addEventListener("submit", function(e){

            if(priceInput){

                let price = parseFloat(priceInput.value);

                if(isNaN(price) || price <= 0){

                    alert("Please enter valid course price");

                    e.preventDefault();
                    return;
                }
            }
        });
    }

    // =========================
    // FILE INPUT UX
    // =========================
    document.querySelectorAll('input[type="file"]').forEach(input => {

        input.addEventListener("change", function(){

            if(this.files.length > 0){

                this.style.borderColor = "#16a34a";
                this.style.background = "#f0fdf4";
            }
        });
    });

    // =========================
    // MULTI SELECT HEIGHT FIX
    // =========================
    document.querySelectorAll("select[multiple]").forEach(select => {

        if(window.innerWidth < 768){

            select.size = 5;

        }else{

            select.size = 8;
        }
    });

});