/* ===== FILE INPUT STYLE ===== */

document
.querySelectorAll('input[type="file"]')
.forEach(input => {

    input.addEventListener("change", function(){

        if(this.files.length > 0){

            this.classList.add("file-selected");

        }else{

            this.classList.remove("file-selected");
        }
    });
});

/* ===== AUTO FOCUS ===== */

window.addEventListener("load", () => {

    const firstInput =
        document.querySelector('input[type="text"]');

    if(firstInput){

        firstInput.focus();
    }
});

/* ===== FORM VALIDATION ===== */

const form = document.querySelector("form");

form.addEventListener("submit", function(e){

    const topicName =
        document.querySelector('input[name="name"]');

    if(topicName.value.trim() === ""){

        alert("Please enter topic name");

        topicName.focus();

        e.preventDefault();

        return;
    }
});

/* ===== BUTTON LOADING ===== */

const submitBtn =
    document.querySelector(".btn");

form.addEventListener("submit", function(){

    submitBtn.innerHTML = "Creating Topic...";

    submitBtn.disabled = true;
});