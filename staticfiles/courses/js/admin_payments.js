document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // TABLE ROW ANIMATION
    // =========================

    const rows = document.querySelectorAll(".payment-row");

    rows.forEach((row, index) => {

        row.style.opacity = "0";
        row.style.transform = "translateY(20px)";

        setTimeout(() => {

            row.style.transition = "all 0.5s ease";

            row.style.opacity = "1";

            row.style.transform = "translateY(0)";

        }, index * 100);

    });

});