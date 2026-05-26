// =========================
// ELEMENTS
// =========================

const freeOption = document.getElementById("freeOption");
const paidOption = document.getElementById("paidOption");

const priceField = document.getElementById("priceField");
const priceInput = document.getElementById("priceInput");

const radioButtons =
document.querySelectorAll('input[name="course_type"]');

// =========================
// TOGGLE PRICE FIELD
// =========================

radioButtons.forEach(radio => {

    radio.addEventListener("change", function(){

        if(this.value === "paid"){

            priceField.classList.remove("hidden");

            paidOption.classList.add("active");
            freeOption.classList.remove("active");

            priceInput.required = true;

        }else{

            priceField.classList.add("hidden");

            freeOption.classList.add("active");
            paidOption.classList.remove("active");

            priceInput.required = false;
            priceInput.value = 0;
        }
    });

});

// =========================
// PRICE VALIDATION
// =========================

if(priceInput){

    priceInput.addEventListener("input", function(){

        if(this.value < 0){
            this.value = 0;
        }

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

form.addEventListener("submit", function(e){

    const selectedType =
    document.querySelector(
        'input[name="course_type"]:checked'
    ).value;

    if(selectedType === "paid"){

        if(
            !priceInput.value ||
            parseFloat(priceInput.value) <= 0
        ){

            alert("Please enter valid course price");

            e.preventDefault();
        }
    }
});

// =========================
// FILE INPUT EFFECT
// =========================

document.querySelectorAll('input[type="file"]')
.forEach(input => {

    input.addEventListener("change", function(){

        if(this.files.length > 0){

            this.style.borderColor = "#16a34a";
        }
    });

});

// =========================
// PAGE ANIMATION
// =========================

window.addEventListener("load", () => {

    const container =
    document.querySelector(".form-container");

    container.style.opacity = "0";
    container.style.transform = "translateY(20px)";

    setTimeout(() => {

        container.style.transition = "0.5s ease";

        container.style.opacity = "1";
        container.style.transform = "translateY(0)";

    }, 100);
});

// =========================
// AUTO FOCUS
// =========================

document.querySelector("input, textarea")?.focus();