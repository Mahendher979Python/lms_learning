document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const submitBtn = document.querySelector(".btn");

    if (!form) return;

    // Prevent double submission
    form.addEventListener("submit", function () {
        submitBtn.disabled = true;
        submitBtn.textContent = "Creating...";
    });

    // Basic required field check (light validation)
    form.addEventListener("submit", function (e) {
        const requiredFields = form.querySelectorAll("input, select");

        let valid = true;

        requiredFields.forEach(field => {
            if (field.hasAttribute("required") && !field.value.trim()) {
                field.style.borderColor = "#dc2626";
                valid = false;
            } else {
                field.style.borderColor = "#d1d5db";
            }
        });

        if (!valid) {
            e.preventDefault();
            submitBtn.disabled = false;
            submitBtn.textContent = "Create Student";
        }
    });
});