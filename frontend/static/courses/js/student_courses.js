document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // SEARCH FILTER
    // =========================

    const searchInput = document.getElementById("searchCourse");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            let value = this.value.toLowerCase();

            let cards = document.querySelectorAll(".course-card");

            cards.forEach(card => {

                card.style.display = card.innerText
                    .toLowerCase()
                    .includes(value)
                    ? "block"
                    : "none";

            });

        });

    }

    // =========================
    // CARD ANIMATION
    // =========================

    const cards = document.querySelectorAll(".course-card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {

            card.style.transition = "0.5s ease";

            card.style.opacity = "1";

            card.style.transform = "translateY(0)";

        }, index * 120);

    });

});