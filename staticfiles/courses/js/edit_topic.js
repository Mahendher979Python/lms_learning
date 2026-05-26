/* ===================================
   RESPONSIVE EDIT TOPIC PAGE JS
=================================== */

document.addEventListener("DOMContentLoaded", function(){

    // ==========================
    // AUTO FOCUS FIRST FIELD
    // ==========================
    const firstInput = document.querySelector('input[type="text"]');

    if(firstInput){
        firstInput.focus();
    }

    // ==========================
    // FILE INPUT PREVIEW EFFECT
    // ==========================
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(input => {

        input.addEventListener("change", function(){

            if(this.files.length > 0){

                // Success border
                this.style.borderColor = "#16a34a";
                this.style.background = "#f0fdf4";

                // File size validation
                const file = this.files[0];

                const maxSize = 1024 * 1024 * 500; // 500MB

                if(file.size > maxSize){

                    alert("File size too large!");

                    this.value = "";
                    this.style.borderColor = "#ef4444";
                    this.style.background = "#fef2f2";
                }
            }
        });

    });

    // ==========================
    // FORM SUBMIT LOADER
    // ==========================
    const form = document.querySelector("form");
    const button = document.querySelector("button");

    if(form){

        form.addEventListener("submit", function(){

            button.innerHTML = "⏳ Updating...";
            button.disabled = true;

        });
    }

});