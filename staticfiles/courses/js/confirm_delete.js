document.addEventListener("DOMContentLoaded", () => {

    const container = document.querySelector(".delete-container");

    container.style.opacity = "0";
    container.style.transform = "scale(0.9)";

    setTimeout(() => {

        container.style.transition = "all 0.4s ease";

        container.style.opacity = "1";

        container.style.transform = "scale(1)";

    }, 100);

});